import * as React from 'react';
import { SideBar } from './SideBar';
import './sass/PrivacyPolicy.scss';

export const PrivacyPolicy = () => {
	return (<div className="privacy-app">
	<div className="privacy-policy">
		<div className="privacy-header">{"Data Collection"}</div>
		<div className="privacy-text">{"BIPPy does not collect any information on its users and stores no stateful server-side information, such as your mnemonic phrases."}</div>
		<div className="privacy-header">{"Transparency"}</div>
		<div className="privacy-text">{"BIPPy is dedicated to total transparency; this is reflected in the "}</div>
		<div className="privacy-header">{"Confidentiality"}</div>
		<div className="privacy-text">{"BIPPy uses incredibly reliable transport encryption (TLS1.2/TLS1.3) to protect your mnemonic data, should you choose to use our web application to generate or recover your wallet information."}</div>
	</div></div>);
}
