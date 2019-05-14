from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="darcamo", channel="stable")
    builder.add_common_builds(pure_c=True)

    # Add the option "dynamic_arch" with value True to every build -> We want
    # binaries compiled by travis to work on many different architectures
    filtered_builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:
        options["openblas:DYNAMIC_ARCH"] = True
        filtered_builds.append([settings, options, env_vars, build_requires])

    builder.builds = filtered_builds
    builder.run()
