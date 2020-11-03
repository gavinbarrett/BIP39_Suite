module.exports = {
	entry: './static/ui/App.jsx',
	mode: 'development',
	module: {
		rules: [
			{
				test: /\.(js|jsx)$/,
				exclude: /node_modules/,
				use: ['babel-loader'],
			},
			{
				test: /\.scss$/,
				exclude: /node_modules/,
				use: [
					{ 
						loader: 'style-loader'
					},
					'css-loader',
					'sass-loader',
				]
			},
			{
				test: /\.css$/,
				use: [
					'style-loader',
					{
						loader: 'css-loader?modules',
						options: {
							importLoaders: 1,
							modules: true
						}
					}
				]
			},
		]
	},
	resolve: {
		extensions: ['.js', '.jsx']
	},
	output: {
		filename: 'App.js',
		path: __dirname + '/static/dist',
	},
};
