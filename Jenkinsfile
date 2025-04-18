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
                        sh """
                            sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no \\
                                ${SSH_USER}@${DEPLOY_SERVER} '
                                    cd ${DEPLOY_PATH} &&
                                    
                                    # Marcar el repositorio como seguro para evitar el error de "dubious ownership"
                                    git config --global --add safe.directory ${DEPLOY_PATH} &&

                                    echo "Realizando pull del repositorio..." &&
                                    echo "$SSH_PASS" | sudo -S git pull https://jonathansilent:${GITHUB_TOKEN}@github.com/Silent4Devs/layservices.git ${GIT_BRANCH} &&

                                    echo "Haciendo cambios..." &&
                                    # Usar sudo para poder escribir en el archivo
                                    echo "$SSH_PASS" | sudo -S bash -c 'echo "Cambio automático desde Jenkins" >> ${DEPLOY_PATH}/jenkins-update.txt' &&

                                    git add . &&
                                    git commit -m "Commit automático desde Jenkins" || echo "No hay cambios que commitear" &&

                                    echo "Haciendo push..." &&
                                    git push https://jonathansilent:${GITHUB_TOKEN}@github.com/Silent4Devs/layservices.git ${GIT_BRANCH}
                                '
                        """
                    }
                }
            }
        }
    }
}

