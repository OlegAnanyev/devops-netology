node("ansible_docker"){
    stage("Git checkout"){
        git credentialsId: '4230dd89-d7a2-4ac5-9ce2-2b30fe9f25a1', url: 'https://github.com/OlegAnanyev/example-playbook.git'
    }
    stage("Check ssh key"){
        secret_check=true
    }
    stage("Run playbook"){
        if (secret_check){
            sh 'ansible-vault decrypt secret --vault-password-file vault_pass'
            sh 'mkdir ~/.ssh/'
            sh 'mv ./secret ~/.ssh/id_rsa'
            sh 'chmod 400 ~/.ssh/id_rsa'
            sh 'ansible-galaxy install -r requirements.yml -p roles'
            sh 'ansible-playbook site.yml -i inventory/prod.yml'
        }
        else{
            echo 'no more keys'
        }
        
    }
}
