import * as React from 'react';
import './sass/Download.scss';

export const Download = () => {
	return (<div className="download-wrapper">
		<div className="download-header">
			{"Download Header"}
		</div>
		<div className="download-options">
			<div className="local-webclient">
				{"Install local client"}
			</div>
			<div className="cli-client">
				{"pip install bippy"}
			</div>
		</div>
	</div>);
}
