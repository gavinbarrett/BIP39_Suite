import * as React from 'react';
import * as Router from 'react-router-dom';
import { SideBar } from './SideBar';
import './sass/LandingPage.scss';

const Summary = () => {
	return (<div className="spacer">
		{"An open source, extensible package dedicated to the future of crypto dev."}
	</div>);
}

export const LandingPage = () => {
	const refer = React.createRef();
	const scrollToInfo = event => {
		event.preventDefault();
		// scroll to the more info section
		refer.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
	}
	return (<><div className="landing-app">
	<SideBar/>
	<div className="landing-page">
		<div className="landing-image">
			<div className="landing-text">{"Audit your crypto wallets"}</div>
			<div className="learn-more">
				<button className="learn-more-button" onClick={scrollToInfo}>{`Learn more`}
					<div className="arrow-down">&#10157;</div>
				</button>
			</div>
		</div>
	</div>
	</div>
	<Summary/>
	<div ref={refer} id="more-info">
		<div id="info">
		<div className="info-header">{"Welcome to the biptools crypto wallet suite!"}</div>
		<div className="info-desc-wrapper">
			<div className="info-desc">{"You can use this web app to generate new BIP32 compatible wallets or recover your pre-existing wallets. The Generation and Recovery pages offer a simple way to view your mnemonic phrase, master seed, master extended keys, and addresses associated with these keys."}</div>
			<div className="landing-link">
				<Router.Link to="/recover">Recover Wallet</Router.Link>
			</div>
			<div className="landing-link">
				<Router.Link to="/generate">Generate Wallet</Router.Link>
			</div>
		</div>
		<div className="info-precaution-wrapper">
			<div className="info-precaution">{"It is highly recommended that you install one of the local clients from the Download Client page. Please understand the risks associated before using this software; biptools is still in early development and requires testing and auditing from security professionals before it can be used in production systems."}</div>
			<div className="landing-link">
				<Router.Link to="/documentation">Documentation</Router.Link>
			</div>
			<div className="landing-link">
				<Router.Link to="/download">Download Client</Router.Link>
			</div>
		</div>
		</div>
	</div></>);
}
