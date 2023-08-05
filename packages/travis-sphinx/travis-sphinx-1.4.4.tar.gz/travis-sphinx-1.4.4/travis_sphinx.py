import os
import sys
import subprocess
import getopt
import sphinx

def run(*args):
    ret = subprocess.call(args, stdout=sys.stdout, stderr=sys.stderr)
    if ret != 0:
        sys.exit(ret)
        
def run_silent(*args):
    ret = subprocess.call(args, stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
    if ret != 0:
        print('error occured while pushing to gh-pages. Has your repo/token changed?')
        sys.exit(ret)

def build_docs(source_dir, target_dir, flags):
    """
    Build documentation from ``source_dir``, placing built files in
    ``target_dir``.

    :param str source_dir: location of sphinx documentation files
    :param str target_dir: location to build to
    """
    print('building documentation')
    args = ['-b html']
    if len(flags):
        args = args + flags
    if sphinx.build_main(args + [source_dir, target_dir]):
        return False
    open('%s/.nojekyll' % target_dir, 'a').close()
    return True

def deploy_docs(target_dir, branches, pr_flag):
    """
    Deploy built docs to gh-pages, uses ``GH_TOKEN`` for pushing built
    documentation files located in *target/doc* to gh

    :param str target_dir: directory that build files were written to
    """
    branch = os.environ['TRAVIS_BRANCH']
    pr = os.environ['TRAVIS_PULL_REQUEST']
    token = os.environ.get('GH_TOKEN')
    repo = os.environ['TRAVIS_REPO_SLUG']
    tag = os.environ['TRAVIS_TAG']

    if token is None:
        print("ERROR: GH_TOKEN is missing!")
        sys.exit(3)

    if (branch in branches and (pr == 'false' or pr_flag)) or tag:
        print('uploading docs...')
        sys.stdout.flush()
        run('git', 'clone', 'https://github.com/davisp/ghp-import')
        run('./ghp-import/ghp_import.py', '-n', 'target/doc/build')
        print('pushing to gh-pages...')
        run_silent('git', 'push', '-fq', 'https://%s@github.com/%s.git'
            % (token, repo), 'gh-pages')
        print('success!')
    else:
        print('build triggered for non-master branch \'' + branch + \
                '\', skipping deploy...')
        sys.exit(1)

def usage():
    """
    Print usage message when a user does not enter any cline args, or
    if they specify --help
    """
    print('Usage: travis-sphinx [options] {actions}\n')
    print('Options:\n  -h, --help\t\tSee usage of script\n' + \
          '  -s, --source\t\tSource directory of sphinx docs, default is docs/source\n' + \
          '  -o, --outdir\t\tDirectory to put html docs, default is target/doc/build\n' + \
          '  -n, --nowarn\t\tDo not error on warnings\n' + \
          '  -b, --branches\tComma separated list of branches to build on\n\t\t\tdefault is =master\n'
          '  -p, --pullrequests\tDeploy on pull requests (not recommended)')
    print('Actions:\n  build \t\tBuild sphinx documentation, places docs in target/doc' + \
          '\n  deploy\t\tDeploy sphinx docs to travis branch by pulling from\n\t\t\ttarget/doc')

def main():
    source_dir = 'docs/source'
    target_dir = 'target/doc/build'
    flags = ['-W']
    branches = ['master']
    pr_flag = False
    # Print usage if no arguments entered
    if len(sys.argv) == 1:
        print('travis-sphinx v1.4.1')
        usage()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'nhs:o:b:p', ['nowarn', 'help', 'source=', 'outdir=', 'branches=', 'pullrequests'])

    except getopt.GetoptError as err:
        print(str(err) + ', see --help for valid arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        if opt in ('-s', '--source'):
            if sys.argv[-1] == 'deploy':
                print('source option not allowed for deploy')
                sys.exit(2)
            source_dir = arg
        if opt in ('-o', '--outdir'):
            if sys.argv[-1] == 'deploy':
                print('outdir option not allowed for deploy')
                sys.exit(2)
            target_dir = arg
        if opt in ('-n', '--nowarn'):
            flags.remove('-W')
        if opt in ('-b', '--branches'):
            branches = [x.strip(' ') for x in arg.split(',')]
        if opt in ('-p', '--pullrequests'):
            pr_flag = True

    if sys.argv[-1] == 'build':
        if not build_docs(source_dir, target_dir, flags):
            sys.exit(2)
    elif sys.argv[-1] == 'deploy':
        deploy_docs(target_dir, branches, pr_flag)
    else:
        usage() 
        sys.exit(2)

if __name__ == '__main__':
    main()
