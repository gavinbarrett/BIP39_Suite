import * as React from 'react';
import './sass/SeedContainer.scss';

interface seedContainer {
	phrase: string;
	seed: string;
	m_xprv: string;
	m_xpub: string;
}

export const SeedContainer = ({phrase, seed, m_xprv, m_xpub}:seedContainer) => {
	const [phraseExposed, updatePhraseExposed] = React.useState("");
	const [seedExposed, updateSeedExposed] = React.useState("");
	const [xprvExposed, updateXprvExposed] = React.useState("");
	const [xpubExposed, updateXpubExposed] = React.useState("");

	const exposePhrase = () => {
		// toggle mnemonic phrase display
		phraseExposed === "" ? updatePhraseExposed("active-field") : updatePhraseExposed("");
	}
	const exposeSeed = () => {
		// toggle root node display
		seedExposed === "" ? updateSeedExposed("active-field") : updateSeedExposed("");
	}
	const exposeXprv = () => {
		// toggle xprv display
		xprvExposed === "" ? updateXprvExposed("active-field") : updateXprvExposed("");
	}
	const exposeXpub = () => {
		// toggle xpub display
		xpubExposed === "" ? updateXpubExposed("active-field") : updateXpubExposed("");
	}

	return (<div className="seedcontainer">
		<div className="seedinfo">
			<div className="seedtext">{phrase}</div>
			<button className={`expose-button ${phraseExposed}`} onClick={exposePhrase}>{"Mmnemonic"}</button>
		</div>
		<div className="seedinfo">
			<div className="seedtext">{seed}</div>
			<button className={`expose-button ${seedExposed}`} onClick={exposeSeed}>{"Root Node"}</button>
		</div>
		<div className="seedinfo">
			<div className="m_xprv">{m_xprv}</div>
			<button className={`expose-button ${xprvExposed}`} onClick={exposeXprv}>{"XPrivate Key"}</button>
		</div>
		<div className="seedinfo">
			<div className="m_xpub">{m_xpub}</div>
			<button className={`expose-button ${xpubExposed}`} onClick={exposeXpub}>{"XPublic Key"}</button>
		</div>
	</div>);
}
