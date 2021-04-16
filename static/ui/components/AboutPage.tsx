import * as React from 'react';
import './sass/AboutPage.scss';

export const AboutPage = ({reference}) => {
	return (<div ref={reference} className="about-page">
		<div className="about-header">{"What are BIP 32 and 39?"}</div>
		<p className="about-para">
			They are two standards introduced to the Bitcoin documentation that provide an overview of how to generate and manage <b><a href="https://en.bitcoinwiki.org/wiki/Deterministic_wallet">Hierarchical Deterministic (HD) wallets</a></b>, respectively. BIP 32 defines the method for generating a mnemonic passphrase; if you own cryptocurrency, you likely have one of these passphrases. BIP 39 defines the method for deriving your private/public key pairs from this passphrase, allowing you to transact with your crypto.
		</p>
		<div className="about-header">{"What exactly is an HD wallet?"}</div>
		<p className="about-para">
			<b>Hierarchical</b> implies that the wallet starts at a beginning, or a root. Like the root of a tree growing into its branches, your wallet starts at a root that can generate all of your cryptocurrency key pairs. With any BIP39 compatible wallet, you have numerous public/private key pairs which are all ultimately derived from the mnemonic passphrase. <b>Deterministic</b> implies that, provided that you have your mnemonic phrase (and maybe an optional password), you will be able to correctly derive all of your public/private key pairs and access your cryptocurrency.
		</p>
	</div>);
}
