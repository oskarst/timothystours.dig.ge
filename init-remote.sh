set -e
mkdir -p /home/dev/timothystours.dig.ge
mv /home/dev/temp-timothystours-pub /home/dev/timothystours.dig.ge/pub
mv /home/dev/PLAYBOOK.md /home/dev/README.md /home/dev/brand.md /home/dev/content-draft.md /home/dev/timothystours.dig.ge/

cd /home/dev/timothystours.dig.ge
echo "node_modules/" > .gitignore

git init
git config user.name "dev"
git config user.email "dev@dig.ge"

git checkout -b main
git add .
git commit -m "Initial commit"

gh repo create oskarst/timothystours.dig.ge --public --source=. --remote=origin --push

git checkout -b dev
git push origin dev

echo -e "timothystours.dig.ge\nhttps://github.com/oskarst/timothystours.dig.ge.git\nstatic\ndev\n" | sudo -n new-vhost
