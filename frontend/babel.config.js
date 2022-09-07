module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      [
        "module-resolver",
        {
          "cwd": "babelrc",
          "root": ["./"],
          "extensions": [".js", ".jsx"],
          "alias": {
            "components": "./src/components"
          }
        }
      ]
    ]
  };
};
