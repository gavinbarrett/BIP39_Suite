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
	const [hiddenPhrase, updateHiddenPhrase] = React.useState('');
	const [hiddenSeed, updateHiddenSeed] = React.useState('');
	const [hiddenXprv, updateHiddenXprv] = React.useState('');
	const [hiddenXpub, updateHiddenXpub] = React.useState('');

	const exposeField = (field, toggleField, toggleHidden) => {
		console.log('toggling');
		if (field === "") {
			toggleHidden("display-info");
			toggleField("active-field");
		} else {
			toggleHidden("");
			toggleField("");
		}
	}
	return (<div className="seedcontainer">
		<div className="seedinfo">
			<div className={`phrase`}>
				<div className={`seed-phrase ${hiddenPhrase}`}>{phrase}</div>
			</div>
			<button className={`expose-button ${phraseSwitch}`} onClick={() => exposeField(phraseSwitch, togglePhraseSwitch, updateHiddenPhrase)}>{"Mmnemonic"}</button>
		</div>
		<div className="seedinfo">
			<div className={`seed ${hiddenSeed}`}>
				<div className={`seed-seed ${hiddenSeed}`}>{seed}</div>
			</div>
			<button className={`expose-button ${seedSwitch}`} onClick={() => exposeField(seedSwitch, toggleSeedSwitch, updateHiddenSeed)}>{"Root Node"}</button>
		</div>
		<div className="seedinfo">
			<div className={`m_xprv`}>
				<div className={`seed-xprv ${hiddenXprv}`}>{m_xprv}</div>
			</div>
			<button className={`expose-button ${xprvSwitch}`} onClick={() => exposeField(xprvSwitch, toggleXprvSwitch, updateHiddenXprv)}>{"XPrivate Key"}</button>
		</div>
		<div className="seedinfo">
			<div className={`m_xpub`}>
				<div className={`seed-xpub ${hiddenXpub}`}>{m_xpub}</div>
			</div>
			<button className={`expose-button ${xpubSwitch}`} onClick={() => exposeField(xpubSwitch, toggleXpubSwitch, updateHiddenXpub)}>{"XPublic Key"}</button>
		</div>
	</div>);
}
