import * as React from 'react';
import { SideBar } from './SideBar';
import './sass/Download.scss';

export const Download = () => {
	return (<div className="download-app">
	<SideBar/>
	<div className="download-wrapper">
		<div className="download-options">
			<div className="local-webclient">
				<div className="download-title">{"Install the local clients"}</div>
				<div className="download-desc">{"Install the Web and CLI clients"}</div>
				<div className="local-installs">
					<p className="download-comment">{"# Clone the repository"}</p>
					<p className="download-command">{"$ git clone https://github.com/gavinbarrett/biptools"}</p>
					<p className="download-comment">{"# Enter the directory"}</p>
					<p className="download-command">{"$ cd biptools"}</p>
					<p className="download-comment">{"# Install the dependencies"}</p>
					<p className="download-command">{"$ npm install && pip install -r requirements.txt"}</p>
					<p className="download-comment">{"# Start the local server"}</p>
					<p className="download-command">{"$ npm run server"}</p>
					<p className="download-comment">{"# Now go to localhost:5000 in your browser!"}</p>
				</div>
			</div>
			<div className="cli-client">
				<div className="download-title">{"Install the Python package"}</div>
				<div className="download-desc">{"Extend your crypto project"}</div>
				<div className="pip-install">
					<p className="download-comment">{"# Install the biptools package"}</p>
					<p className="download-command">{"$ pip install biptools"}</p>
					<p className="download-comment">{"# Start the Python shell"}</p>
					<p className="download-command">{"$ python"}</p>
					<p className="download-comment">{"# Import a BIP32 subclass"}</p>
					<p className="download-command">{">>> from biptools import BIP44"}</p>
					<p className="download-comment">{"# Generate a BIP32 compatible wallet"}</p>
					<p className="download-command">{">>> wallet = BIP44('twelve pride tower pass fruit ozone exclude lemon pool wall abandon want answer vapor chunk')"}</p>
					<p className="download-comment">{"# Generate master extended keys"}</p>
					<p className="download-command">{">>> xprv, xpub = wallet.get_master_keys()"}</p>
				</div>
			</div>
		</div>
	</div></div>);
}
