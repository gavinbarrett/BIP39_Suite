import * as React from 'react';
import './sass/LandingPage.scss';

export const LandingPage = () => {
	
	const scrollToInfo = event => {
		const elem = document.getElementById("more-info");
		if (elem)
			elem.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}

	return (<div className="landing-page">
		<div className="landing-box">
			<div className="landing-header">
				{"Manage your entire crypto portfolio"}
			</div>
			<div className="landing-image">
				<img src={"./static/ui/components/sass/assets/botcrypto.jpg"}/>
			</div>
		</div>
		<div className="learn-more" onClick={scrollToInfo}>{"Learn more."}</div>
		<div id="more-info">
			{"Here's some info."}
		</div>
	</div>);
}
