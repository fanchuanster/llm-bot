set bname=wen_dev
set bmain=master
git checkout %bmain%
git branch -d %bname%
git fetch
git pull
git push --delete origin %bname%

@REM create my local and remote branches.
git checkout -b %bname%
git push --set-upstream origin %bname%

