from distutils.core import setup
setup(name='fume',
        version='0.1',
        description="Fume: a smoke test scripting language",
        author="Christian Fernandez",
        author_email="c@hackbrightacademy.com",
        packages=["fume"],
        package_dir={"": "src"},
        scripts=['scripts/fume'],
        requires=["docopt (>= 0.6.1)", "requests (>=2.0.0)"]
        )
