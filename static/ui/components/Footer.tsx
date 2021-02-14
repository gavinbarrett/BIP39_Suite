import * as React from 'react';
import './sass/Footer.scss';

export const Footer = () => {
	return (<footer>
		<div className="footer-box">
			<div className="footer-field">
				Source Code
			</div>
			<div className="footer-field">
				Privacy Policy
			</div>
			<div className="footer-field">
				BipSuite &copy; 2021
			</div>
		</div>
	</footer>);
}
