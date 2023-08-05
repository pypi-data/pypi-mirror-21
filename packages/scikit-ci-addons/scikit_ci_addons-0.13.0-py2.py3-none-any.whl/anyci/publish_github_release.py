"""
This add-on allows to automatically create GitHub releases or prereleases
and upload associated packages. It respectively provides a "release" and
a "prerelease" sub-command.
"""

import argparse
import datetime as dt
import errno
import os
import platform
import sys
import subprocess
import textwrap

from github_release import (
    gh_asset_delete,
    gh_asset_upload,
    get_refs,
    gh_release_create,
    gh_release_edit
)


#
# Git
#

GITS = ["git"]
if sys.platform == "win32":
    GITS = ["git.cmd", "git.exe"]


# Copied from https://github.com/warner/python-versioneer/blob/master/src/subprocess_helper.py  # noqa: E501
def run_command(commands, args, cwd=None, verbose=False, hide_stderr=False,
                env=None):
    """Call the given command(s)."""
    assert isinstance(commands, list)
    for c in commands:
        dispcmd = str([c] + args)
        try:
            # remember shell=False, so use git.cmd on windows, not just git
            p = subprocess.Popen([c] + args, cwd=cwd, env=env,
                                 stdout=subprocess.PIPE,
                                 stderr=(subprocess.PIPE if hide_stderr
                                         else None))
            break
        except EnvironmentError:
            e = sys.exc_info()[1]
            if e.errno == errno.ENOENT:
                continue
            if verbose:
                print("unable to run %s" % dispcmd)
                print(e)
            return None, None
    else:
        if verbose:
            print("unable to find command, tried %s" % (commands,))
        return None, None
    stdout = p.communicate()[0].strip()
    if sys.version_info[0] >= 3:
        stdout = stdout.decode()
    if p.returncode != 0:
        if verbose:
            print("unable to run %s (error)" % dispcmd)
            print("stdout was %s" % stdout)
        return None, p.returncode
    return stdout, p.returncode


def get_tag(ref="HEAD"):
    output, _ = run_command(
        GITS, ["describe", "--tags", "--exact-match", str(ref)],
        hide_stderr=True)
    return output


def get_commit_date(ref="HEAD"):
    output, _ = run_command(
        GITS, ["log", "-1", "--format=%ad", "--date=local", str(ref)])
    return dt.datetime.strptime(output, "%c").strftime("%Y%m%d")


#
# Python
#

def python_wheel_platform():
    this_platform = platform.system().lower()
    return {
        "linux": "manylinux1", "darwin": "macosx", "windows": "win"
    }.get(this_platform, this_platform)


#
# Entry point
#

def configure_parser(parser):
    parser.add_argument(
        "repo_name", type=str, metavar="ORG/PROJECT",
        help="Name of the repository"
    )
    # "release" arguments
    release_group = parser.add_argument_group('release')
    release_group.add_argument(
        "--release-packages", metavar="PATTERN", type=str, nargs="*",
        help="Path(s) and/or wildcard expression(s)"
    )
    # "prerelease" arguments
    prerelease_group = parser.add_argument_group('prerelease')
    prerelease_group.add_argument(
        "--prerelease-packages", metavar="PATTERN", type=str, nargs="*",
        help="Path(s) and/or globbing pattern(s)"
    )
    prerelease_group.add_argument(
        "--prerelease-packages-clear-pattern",
        type=str, metavar="PATTERN",
        help="Globbing pattern selecting the set of packages to remove"
    )
    prerelease_group.add_argument(
        "--prerelease-packages-keep-pattern",
        type=str, metavar="PATTERN",
        help="Globbing pattern identifying the subset of packages to keep"
    )
    prerelease_group.add_argument(
        "--prerelease-tag", type=str,
        help="Name of the tag to associate with the pre-release. "
             "If needed, tag is created or updated (default: nightly)"
    )
    prerelease_group.add_argument(
        "--prerelease-name", type=str,
        help="Name of the pre-release "
             "(default: 'TagName (updated on YYYYMMDD)'. "
             "Example: 'Nightly (updated on 20170212)')"
    )
    prerelease_group.add_argument(
        "--prerelease-sha", type=str,
        help="Commit or branch name to associate with the pre-release "
             "(default: master)"
    )
    # Common arguments
    parser.add_argument(
        "--token", type=str, metavar="GITHUB_TOKEN",
        help="If not specified, expects GITHUB_TOKEN env. variable"
    )
    parser.add_argument(
        "--display-python-wheel-platform", action="store_true",
        help="Display current python platform (manylinux1, macosx, or win)"
             " used for Python wheels."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="don't create release, upload or erase packages "
             "but act like it was done"
    )
    parser.set_defaults(
        token=os.environ.get("GITHUB_TOKEN", None),
        prerelease_packages_clear_pattern=None,
        prerelease_packages_keep_pattern=None,
        prerelease_name=None,
        prerelease_sha="master",
        prerelease_tag="nightly"
    )


def _upload_release(args):
    release_tag = get_tag()
    assert release_tag is not None
    # Create release
    gh_release_create(
        args.repo_name,
        release_tag,
        publish=True, prerelease=False
    )
    # Upload packages
    gh_asset_upload(
        args.repo_name, release_tag, args.release_packages, args.dry_run)
    return True


def _upload_prerelease(args):
    # Set default prerelease name
    prerelease_name = args.prerelease_name
    if prerelease_name is None:
        prerelease_name = "%s (updated on %s)" % (
            args.prerelease_tag.title(), get_commit_date()
        )
    # Create release
    gh_release_create(
        args.repo_name,
        args.prerelease_tag,
        name=prerelease_name,
        publish=True, prerelease=True
    )
    # Upload packages
    gh_asset_upload(
        args.repo_name, args.prerelease_tag, args.prerelease_packages,
        args.dry_run
    )
    # Remove obsolete assets
    if args.prerelease_packages_clear_pattern is not None:
        gh_asset_delete(
            args.repo_name,
            args.prerelease_tag,
            args.prerelease_packages_clear_pattern,
            keep_pattern=args.prerelease_packages_keep_pattern,
            dry_run=args.dry_run
        )
    # if needed, update target commit and name associated with the release
    sha = args.prerelease_sha
    if sha is not None:
        # If a branch name is specified, get associated commit
        refs = get_refs(args.repo_name, pattern="refs/heads/%s" % sha)
        if refs:
            assert len(refs) == 1
            branch = sha
            sha = refs[0]["object"]["sha"]
            print("resolved '%s' to '%s'" % (branch, sha))
        gh_release_edit(
            args.repo_name,
            args.prerelease_tag,
            target_commitish=sha,
            name=prerelease_name
        )
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    configure_parser(parser)
    args = parser.parse_args(argv[1:] if argv else None)

    if args.display_python_wheel_platform:
        print(python_wheel_platform())
        exit(0)

    # Check required parameters
    upload_release = (len(args.release_packages) > 0
                      if args.release_packages else False)
    upload_prerelease = (len(args.prerelease_packages) > 0
                         if args.prerelease_packages else False)
    if not upload_release and not upload_prerelease:
        parser.print_usage()
        print("error: at least --release-packages or --prerelease-packages "
              "argument is required")
        sys.exit(1)
    dual = upload_release and upload_prerelease

    if not args.token:
        print("-" * 80)
        print(textwrap.dedent(
            r"""
            error: A token is expected.

            Specify the --token parameter or set GITHUB_TOKEN environment variable.
            See https://help.github.com/articles/creating-an-access-token-for-command-line-use/
            """  # noqa: E501
        ).lstrip())
        print("-" * 80)
        parser.print_usage()
        exit(1)
    os.environ["GITHUB_TOKEN"] = args.token

    msg = "Checking if HEAD is a release tag"
    print(msg)

    # Upload
    uploaded = False
    is_release = get_tag() is not None
    if upload_release:
        if is_release:
            print("%s - yes (found %s: creating release)\n" % (msg, get_tag()))
            uploaded = _upload_release(args)
        elif not dual:
            print("%s - no (skipping release upload)\n" % msg)

    if not uploaded and upload_prerelease:
        if not is_release:
            print("%s - no (creating prerelease)\n" % msg)
            _upload_prerelease(args)
        elif not dual:
            print("%s - yes (found %s: "
                  "skipping prerelease upload)\n" % (msg, get_tag()))


if __name__ == "__main__":
    main()
