# I ended up running:
# python setup.py register
# ... and then run this ./release.sh script

# modify version only in setup.py
version=`grep version setup.py|awk '{ print $3 }'| sed -e 's/\,//g' | sed -e "s/'//g"`
version=$(($version + 1))
sed -i "s/version.*/version             = '$version',/g" setup.py
sed -i "s/cli_version = .*/cli_version = '$version'/g" aim

rm -rf build dist aimelia.egg-info
python setup.py sdist upload
