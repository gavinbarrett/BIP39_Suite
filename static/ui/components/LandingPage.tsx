import * as React from 'react';
import { SideBar } from './SideBar';
import './sass/LandingPage.scss';

export const LandingPage = () => {
	const refer = React.createRef();
	const scrollToInfo = event => {
		event.preventDefault();
		console.log(refer);
		refer.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
		//console.log(refer.current.offsetTop);
		//window.scrollTo({ top: 0, left: refer.current.offsetTop, behavior: 'smooth' });
	}
	return (<><div className="landing-app">
	<SideBar/>
	<div className="landing-page">
		<div className="landing-image">
			<div className="landing-text">{"Audit your crypto wallets"}</div>
			<div className="learn-more">
				<button className="learn-more-button" onClick={scrollToInfo}>{"Learn more"}</button>
			</div>
		</div>
	</div>
	</div>
	<div ref={refer} id="more-info">
		<div id="info">{"Welcome to the BIPPy crypto wallet suite! You can use this web app to generate new BIP32 compatible wallets or recover your pre-existing wallets. The Generation and Recovery pages offer a simple way to view your mnemonic phrase, master seed, master extended keys, and addresses associated with these keys. It is highly recommended that you install one of the local clients from the Downloads page."}</div>
	</div></>);
}
