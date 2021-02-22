docker run --name metha-system -it --network host \
--mount type=bind,source="$(pwd)"/,target=/root/metha \
metha:latest
