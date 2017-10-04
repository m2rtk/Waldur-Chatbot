#!/bin/bash

echo "Deploying"
# if supplied argument is 'dev', use develop branch
SCRIPT="./local_deploy_backend.sh"
USER=$PRODUSER
REMOTE=$PRODREMOTE
if [ ! -z $1 ]; then
    if [ $1 = "dev" ]; then
        SCRIPT="./local_deploy_backend.sh dev"
        USER=$DEVUSER
        REMOTE=$DEVREMOTE
    fi
fi

echo "Decrypting private key"
openssl aes-256-cbc -K $encrypted_5899b1a8b456_key -iv $encrypted_5899b1a8b456_iv -in .travis/travis_deploy_key.enc -out .travis/travis_deploy_key -d
chmod 600 .travis/travis_deploy_key
echo "Moving local_deploy to remote"
scp -o "StrictHostKeyChecking no" -i .travis/travis_deploy_key .travis/local_deploy_backend.sh $USER@$REMOTE:~/
echo "Executing local_deploy in remote"
ssh -o "StrictHostKeyChecking no" -i .travis/travis_deploy_key $USER@$REMOTE $SCRIPT
