import * as React from 'react';
import { SideBar } from './SideBar';
import './sass/LandingPage.scss';

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
	<div ref={refer} id="more-info">
		<div id="info">
		<div className="info-header">{"Welcome to the biptools crypto wallet suite!"}</div>
		<div className="info-desc">{"You can use this web app to generate new BIP32 compatible wallets or recover your pre-existing wallets. The Generation and Recovery pages offer a simple way to view your mnemonic phrase, master seed, master extended keys, and addresses associated with these keys."}</div>
		<div className="info-precaution">{"It is highly recommended that you install one of the local clients from the Downloads page. Please understand the risk associated with using this software and refrain from using it if you aren't sure what you're doing. BIPPy is still in early development and will need extensive testing and auditing from security professionals before it can be used in production systems. As such, BIPPy takes no responsibility for any lost funds associated with any of your wallets if you choose to use our webapp or build a system from our core package."}</div>
		</div>
	</div></>);
}
