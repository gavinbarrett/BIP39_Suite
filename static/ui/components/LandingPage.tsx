import * as React from 'react';
import './sass/LandingPage.scss';

export const LandingPage = () => {
	const scrollToInfo = event => {
		event.preventDefault();
		document.getElementById("more-info").scrollIntoView({ behavior: 'smooth', block: 'start' });
	}
	return (<div className="landing-page">
		<div className="landing-image">
			<div className="landing-text">{"Audit your crypto wallets"}</div>
			<div className="learn-more">
				<button className="learn-more-button" onClick={scrollToInfo}>{"Learn more"}</button>
			</div>
		</div>
		<div id="more-info">
			<div id="info">{"Here's some info."}</div>
		</div>
	</div>);
}
