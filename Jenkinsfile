pipeline {
    agent any

    environment {
        DEPLOY_SERVER = '192.168.40.1'
        DEPLOY_PATH = '/var/contenedores/layservices'
        GIT_BRANCH = 'main' 
    }

    stages {
        stage('Pull y Push via SSH') {
            steps {
                script {
                    withCredentials([ 
                        usernamePassword(credentialsId: 'LS-CREDENCIALES', usernameVariable: 'SSH_USER', passwordVariable: 'SSH_PASS'),
                        string(credentialsId: 'GITHUB_PAT_TOKEN', variable: 'GITHUB_TOKEN')  
                    ]) {
                        sh '''
                            export GITHUB_TOKEN=${GITHUB_TOKEN}
                            export SSH_PASS=${SSH_PASS}
                            
                            sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no ${SSH_USER}@${DEPLOY_SERVER} bash -c "'
                                if [ ! -d \\"${DEPLOY_PATH}\\" ]; then
                                    echo \\"$SSH_PASS\\" | sudo -S mkdir -p \\"${DEPLOY_PATH}\\"
                                    echo \\"$SSH_PASS\\" | sudo -S chown -R ${SSH_USER}:${SSH_USER} \\"${DEPLOY_PATH}\\"
                                fi

                                cd \\"${DEPLOY_PATH}\\" || exit 1

                                git config --global safe.directory \\"${DEPLOY_PATH}\\"
                                git config user.name \\"Jenkins Bot\\"
                                git config user.email \\"jenkins@silent4devs.local\\"

                                echo \\"$SSH_PASS\\" | sudo -S chmod -R 777 \\"${DEPLOY_PATH}\\"

                                echo \\"Realizando pull del repositorio...\\"
                                echo \\"$SSH_PASS\\" | sudo -S git pull --rebase https://jonathansilent:${GITHUB_TOKEN}@github.com/Silent4Devs/layservices.git ${GIT_BRANCH}

                                git add .
                                git commit -m \\"Commit automático desde Jenkins\\" || echo \\"No hay cambios que commitear\\"

                                echo \\"Haciendo push...\\"
                                git push https://jonathansilent:${GITHUB_TOKEN}@github.com/Silent4Devs/layservices.git ${GIT_BRANCH}
                            '"
                        '''
                    }
                }
            }
        }
    }
}

