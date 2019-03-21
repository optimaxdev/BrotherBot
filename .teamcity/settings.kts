import jetbrains.buildServer.configs.kotlin.v2018_2.*
import jetbrains.buildServer.configs.kotlin.v2018_2.triggers.vcs
import jetbrains.buildServer.configs.kotlin.v2018_2.buildSteps.script

version = "2018.2"

project {
    buildType(Build)
    buildType(Deploy)
}

object Build : BuildType({
    name = "Build BrotherBot"

    artifactRules = "./ => %build.counter%.brother.tar.gz"

    vcs {
        root(DslContext.settingsRoot)
    }

    triggers {
        vcs {
        }
    }
    steps {
        script {
            name = "pip install and test"
            dockerImage = "python:3.6"
            scriptContent = "pip install -r requirements.txt && python -m unittest discover -s ./ -p 'test_*.py'"
        }
    }
})

object Deploy : BuildType({
    name = "deploy"
    description = "Deploy to GCE instance"

    vcs {
        root(DslContext.settingsRoot)

        cleanCheckout = true
    }
    steps {
        step {
            type = "ssh-deploy-runner"
            param("jetbrains.buildServer.deployer.username", "optimax")
            param("teamcitySshKey", "Common")
            param("jetbrains.buildServer.deployer.sourcePath", "%build.counter%.brother.tar.gz => ~/upload/")
            param("jetbrains.buildServer.deployer.targetUrl", "brother.gusadev.com")
            param("jetbrains.buildServer.sshexec.authMethod", "UPLOADED_KEY")
            param("jetbrains.buildServer.deployer.ssh.transport", "jetbrains.buildServer.deployer.ssh.transport.scp")
        }
    }
    triggers {
        vcs {
        }
    }

    dependencies {
        dependency(Tests) {
            snapshot {
                onDependencyFailure = FailureAction.CANCEL
            }

            artifacts {
                artifactRules = "%build.counter%.brother.tar.gz => ./"
            }
        }
    }
})