import * as React from 'react';
import * as Router from 'react-router-dom';
import './sass/Footer.scss';

export const Footer = () => {
	return (<footer>
		<div className="footer-box">
			<a className="footer-field" href="https://github.com/gavinbarrett/BIP39_Suite">
				Source Code
			</a>
			<div className="footer-field">
				<Router.Link className="privacy" to="/privacy">Privacy Policy</Router.Link>
			</div>
			<div className="footer-field">
				BipSuite &copy; 2021
			</div>
		</div>
	</footer>);
}
