node("ansible_docker"){
    stage("Git checkout"){
        git credentialsId: '4230dd89-d7a2-4ac5-9ce2-2b30fe9f25a1', url: 'git@github.com/OlegAnanyev/example-playbook.git'
    }
    stage("Check ssh key"){
        secret_check=true
    }
    stage("Run playbook"){
        if (secret_check){
            sh 'ansible-playbook site.yml -i inventory/prod.yml'
        }
        else{
            echo 'no more keys'
        }
        
    }
}
