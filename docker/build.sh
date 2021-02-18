mkdir ../../qms.docker
pushd ../../qms.docker
git clone --recurse-submodules https://github.com/nextgis/quickmapservices_server.git
cd quickmapservices_server
git checkout py3dj22
popd
cp ./custom_files/settings_local.py ../../qms.docker/quickmapservices_server/qms_server/qms_server/settings_local.py
cp ./custom_files/views.py ../../qms.docker/quickmapservices_server/qms_server/nextgis_common/ngid_auth/views.py
cp -r ./custom_files/frontend_dist ../../qms.docker/quickmapservices_server/qms_server/frontend/dist
cd ../..
docker build --no-cache -t registry.nextgis.com/qms:dj22py36 -f quickmapservices_server/docker/Dockerfile .
rm -rf ../../qms.docker

docker run \
-dit \
--network="host" \
--name qms_dj22py36 \
-e DATABASE_NAME='qms_server3' \
-e DATABASE_USER='qms_server' \
-e DATABASE_PASS='tf7yi8kd' \
-e DATABASE_HOST='localhost' \
-e DATABASE_PORT='5432' \
-e ALLOWED_HOST='127.0.0.1' \
-P \
registry.nextgis.com/qms:dj22py36

