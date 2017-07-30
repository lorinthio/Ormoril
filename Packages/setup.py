from setuptools import setup

versionFile = open("version.txt", "r")
versionText = versionFile.readline()
versionFile.close()
versionNumbers = versionText.split(".")
for i in range(len(versionNumbers)):
    versionNumbers[i] = int(versionNumbers[i])
versionNumbers[2] += 1
versionText = "{}.{}.{}".format(versionNumbers[0], versionNumbers[1], versionNumbers[2])

versionFile = open("version.txt", "w")
versionFile.write(versionText)
versionFile.close()

setup(name="OrmorilCommon",
      version=versionText,
      description="A package used to share packet information and other utilities between client and server",
      url="http://github.com/lorinthio/TextBasedRpg",
      author="Lorinthio",
      author_email="lorinthio@yahoo.com",
      license="MIT",
      packages=["Common"],
      zip_safe=False)

