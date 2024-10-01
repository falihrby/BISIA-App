// C:\Users\LENOVO\OneDrive\Documents\Falih\BISIA-App\frontend\config-overrides.js

module.exports = function override(config, env) {
    const babelLoader = config.module.rules.find(
      rule => rule.oneOf !== undefined
    ).oneOf.find(loader => loader.loader && loader.loader.includes("babel-loader"));
  
    if (babelLoader) {
      babelLoader.options.plugins = [
        ...(babelLoader.options.plugins || []),
        ["@babel/plugin-proposal-private-property-in-object", { loose: true }],
        ["@babel/plugin-transform-class-properties", { loose: true }],
        ["@babel/plugin-transform-private-methods", { loose: true }]
      ];
    }
  
    return config;
  };
  