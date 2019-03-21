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
            branchFilter = """
        +:*
        +:refs/tags/*
    """.trimIndent()
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
            param("jetbrains.buildServer.deployer.sourcePath", "%dep.OPT_MS_TestsAndBuilds_Office_BrotherBot_Build.build.counter%.brother.tar.gz => ~/upload/")
            param("jetbrains.buildServer.deployer.targetUrl", "brother.gusadev.com")
            param("jetbrains.buildServer.sshexec.authMethod", "UPLOADED_KEY")
            param("jetbrains.buildServer.deployer.ssh.transport", "jetbrains.buildServer.deployer.ssh.transport.scp")
        }
        step {
            type = "ssh-exec-runner"
            param("jetbrains.buildServer.deployer.username", "optimax")
            param("jetbrains.buildServer.sshexec.command", "%deploy_brother%")
            param("teamcitySshKey", "Common")
            param("jetbrains.buildServer.deployer.targetUrl", "brother.gusadev.com")
            param("jetbrains.buildServer.sshexec.authMethod", "UPLOADED_KEY")
        }
    }
    triggers {
        vcs {
            branchFilter = "+:refs/tags/*"
        }
    }

    dependencies {
        dependency(Build) {
            snapshot {
                onDependencyFailure = FailureAction.CANCEL
            }

            artifacts {
                artifactRules = "%dep.OPT_MS_TestsAndBuilds_Office_BrotherBot_Build.build.counter%.brother.tar.gz => ./"
            }
        }
    }
})