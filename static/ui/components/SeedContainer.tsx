import * as React from 'react';
import './sass/SeedContainer.scss';

interface seedContainer {
	phrase: string;
	seed: string;
	m_xprv: string;
	m_xpub: string;
}

export const SeedContainer = ({phrase, seed, m_xprv, m_xpub}:seedContainer) => {

	const [phraseSwitch, togglePhraseSwitch] = React.useState('');
	const [seedSwitch, toggleSeedSwitch] = React.useState('');
	const [xprvSwitch, toggleXprvSwitch] = React.useState('');
	const [xpubSwitch, toggleXpubSwitch] = React.useState('');

	const exposeField = (field, toggleField) => {
		if (field === "") {
			toggleField("active-field")
		} else {
			toggleField("");
		}
	}
	return (<div className="seedcontainer">
		<div className="seedinfo">
			<div className="seedtext">{phrase}</div>
			<button className={`expose-button ${phraseSwitch}`} onClick={() => exposeField(phraseSwitch, togglePhraseSwitch)}>{"Mmnemonic"}</button>
		</div>
		<div className="seedinfo">
			<div className="seedtext">{seed}</div>
			<button className={`expose-button ${seedSwitch}`} onClick={() => exposeField(seedSwitch, toggleSeedSwitch)}>{"Root Node"}</button>
		</div>
		<div className="seedinfo">
			<div className="m_xprv">{m_xprv}</div>
			<button className={`expose-button ${xprvSwitch}`} onClick={() => exposeField(xprvSwitch, toggleXprvSwitch)}>{"XPrivate Key"}</button>
		</div>
		<div className="seedinfo">
			<div className="m_xpub">{m_xpub}</div>
			<button className={`expose-button ${xpubSwitch}`} onClick={() => exposeField(xpubSwitch, toggleXpubSwitch)}>{"XPublic Key"}</button>
		</div>
	</div>);
}
