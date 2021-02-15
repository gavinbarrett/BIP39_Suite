import * as React from 'react';
import './sass/Download.scss';

export const Download = () => {
	return (<div className="download-wrapper">
		<div className="download-header">
			{"Download Header"}
		</div>
		<div className="download-options">
			<div className="local-webclient">
				<div className="download-title">{"Install the local clients"}</div>
				<div className="download-desc">{"Install the Web and CLI clients"}</div>
				<div className="local-installs">
					{"$ git clone https://github.com/gavinbarrett/BIP39_Suite"}
				</div>
			</div>
			<div className="cli-client">
				<div className="download-title">{"Install the python package"}</div>
				<div className="download-desc">{"Extend your crypto project"}</div>
				<div className="pip-install">
					{"$ pip install bippy"}
				</div>
			</div>
		</div>
	</div>);
}
