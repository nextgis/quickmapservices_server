mkdir ../../qms.docker
pushd ../../qms.docker
git clone --recurse-submodules https://github.com/nextgis/quickmapservices_server.git
cd quickmapservices_server
git checkout py3dj22
popd
cp ./custom_files/settings_local.py ../../qms.docker/quickmapservices_server/qms_server/qms_server/settings_local.py
cp ./custom_files/views.py ../../qms.docker/quickmapservices_server/qms_server/nextgis_common/ngid_auth/views.py
cd ../..
docker build --no-cache -t qms:dj22py36 -f quickmapservices_server/docker/Dockerfile .
rm -rf qms.docker

