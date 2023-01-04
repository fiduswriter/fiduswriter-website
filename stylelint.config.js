module.exports = { // eslint-disable-line no-undef
    "extends": "stylelint-config-standard",
    "rules": {
        "max-empty-lines": 4,
        "string-quotes": "single",
        "color-hex-length": "long",
        "number-leading-zero": "never",
        "max-nesting-depth": 2,
        "indentation": 4,
        "selector-class-pattern": [
            "^(([a-z][a-z0-9]*)(-[a-z0-9]+)*)|(ProseMirror(-[a-z0-9]+)*)$",
            {
                message: "Selector should use lowercase and separate words with hyphens (selector-class-pattern)",
            },
        ],
    }
}
