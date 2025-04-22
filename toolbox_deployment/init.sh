#! /bin/bash

sleep 5

if mc config host add local http://minio:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD; then
  echo 'Host added successfully!'
else
  echo 'Host not added successfully!'
  exit 1
fi

if mc mb local/models; then
  echo 'Initial bucket created'
else
  echo 'Initial bucket not created'
fi

