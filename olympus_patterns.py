"""Regex patterns for Olympus naming convention."""
patterns = {
    "os": {
        "centos" : "[Cc][Ee][Nn][Tt][Oo][Ss]",
        "RHEL" : "([Rr][Ee][Dd][ Hh][HhAa][AaTt][ Tt])|([Rr][Hh][Ee][Ll])",
        "ubuntu" : "[Uu][Bb][Uu][Nn][Tt][Uu]",
        "windows" : "[Ww][Ii][Nn][Dd][Oo][Ww][Ss]"
    },

    "ivm" : {
        "engine" : "[Ee][Nn][Gg][Ii][Nn][Ee]",
        "console" : "[Cc][Oo][Nn][Ss][Oo][Ll][Ee]",
        "nsc/nse" : "[Nn][Ss][CcEe]"
    }
}
