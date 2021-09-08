docker image ls -q | xargs -I {} docker image rm -f {}
