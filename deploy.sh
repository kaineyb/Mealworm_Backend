#!/bin/bash

function get_branch() {
      git branch --no-color | grep -E '^\*' | awk '{print $2}' \
        || echo "default_value"
      # or
      # git symbolic-ref --short -q HEAD || echo "default_value";
}



function deploy_production() {
    # Set Variables
    
    export DEPLOYPATH=~/python/api_mealworm
    
    # Clear Dev Directory
    rm -r ~/python/api_mealworm/*
    
    # Copy Files over from local dev repo
    /bin/cp -r ~/repositories/Mealworm_Backend/* ~/python/api_mealworm
    
    # Delete git folder
    rm -r ~/python/api_mealworm/.git

    # prod python environment
    source /home2/arkus/virtualenv/python/api_mealworm/3.8/bin/activate && cd /home2/arkus/python/api_mealworm

    # Can't use pipenv anymore?
    # echo "##########"
    # echo "installing pipenv"
    # echo "##########"
    # pip install pipenv

    # echo "##########"
    # echo "installing dependencies from lockfile"
    # echo "##########"
    # pipenv install


    # echo "##########"
    # echo "migrating django"
    # echo "##########"
    # echo "migrating django"
    # python manage.py migrate

    # # pip only solution
    echo "##########"
    echo "installing pipenv"
    echo "##########"
    pip install pipenv

    echo "##########"
    echo "creating requirements"
    echo "##########"
    pipenv requirements > requirements.txt

    echo "##########"
    echo "installing packages using pip"
    echo "##########"
    pip install -r requirements.txt


    echo "##########"
    echo "migrating django"
    echo "##########"
    python manage.py migrate

    # Tell me that it worked...!
    echo "Production Deployed!"
}

branch_name=`get_branch`;
echo $branch_name;

if [ $branch_name == 'main' ]
then 
    deploy_production
fi