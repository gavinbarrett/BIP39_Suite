import * as React from 'react';
import './sass/LandingPage.scss';

export const LandingPage = () => {
	return (<div className="landing-page">
		<div className="landing-box">
			<div className="landing-header">
				{"Manage your entire crypto portfolio"}
			</div>
			<div className="landing-image">
				<img src={"./static/ui/components/sass/assets/botcrypto.jpg"}/>
			</div>
		</div>
		<div className="learn-more">{"Learn more."}</div>
		<div className="more-info">
		</div>
	</div>);
}
