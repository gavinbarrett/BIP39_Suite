import * as React from 'react';
import './sass/KeyGenerator.scss';

interface byteScheme {
	desc: string;
	bytes: number;
	active: number;
	updateSelected: (number) => number;
}

interface byteSelector {
	selected: number;
	updateSelected: (number) => number;
}

interface seedContainer {
	phrase: string;
	seed: string;
	m_xprv: string;
	m_xpub: string;
}

const ByteScheme = ({desc, bytes, active, updateSelected}:byteScheme) => {
	const byteclass = (bytes === active) ? "activebyte" : "bytes";
	const updateActivity = async () => {
		await updateSelected(bytes);
	}
	return (<div className={byteclass} onClick={updateActivity}>{desc}</div>);
}

const ByteSelector = ({selected, updateSelected}:byteSelector) => {
	// bytes of entropy/words in seed phrase - 16/12, 20/15, 24/18, 28/21, 32/24
	return (<div id="byteselector">
		<ByteScheme desc={"12 words"} bytes={16} active={selected} updateSelected={updateSelected}/>
		<ByteScheme desc={"15 words"} bytes={20} active={selected} updateSelected={updateSelected}/>
		<ByteScheme desc={"18 words"} bytes={24} active={selected} updateSelected={updateSelected}/>
		<ByteScheme desc={"21 words"} bytes={28} active={selected} updateSelected={updateSelected}/>
		<ByteScheme desc={"24 words"} bytes={32} active={selected} updateSelected={updateSelected}/>
	</div>);
}

const SeedContainer = ({phrase, seed, m_xprv, m_xpub}:seedContainer) => {
	return (<div className="seedcontainer">
		<div className="seedtext">{phrase}</div>
		<div className="seedtext">{seed}</div>
		<div className="m_xprv">{m_xprv}</div>
		<div className="m_xpub">{m_xpub}</div>
	</div>);
}

export const KeyGenerator = () => {
	const [pass, updatePass] = React.useState('');
	const [selected, updateSelected] = React.useState(32);
	const [phrase, updatePhrase] = React.useState(null);
	const [seed, updateSeed] = React.useState(null);
	const [m_xprv, updateMxprv] = React.useState(null);
	const [m_xpub, updateMxpub] = React.useState(null);

	const update_pass = async (event) => { updatePass(event.target.value); }

	const submit_params = async () => {
		// gather desired passphrase and word count
		const resp = await fetch('/generate', {method: 'POST', headers: {"Content-Type": "application/json"}, body: JSON.stringify({"bytes": selected, "passphrase": pass})});
		const data = await resp.json();
		console.log(data);
		if (data["phrase"] === "failed") {
			console.log('failed');
			return;
		}
		updatePhrase(data["phrase"]);
		updateSeed(data["seed"]);
		updateMxprv(data["m_xprv"]);
		updateMxpub(data["m_xpub"]);
	}

	return (<div className="generator">
		<div className='selector-box'>
		<ByteSelector selected={selected} updateSelected={updateSelected}/>
			<div className='parameters'>
				<div className="passlabel">Passphrase</div>
				<input className="pass" id="passphrase" type="password" onChange={update_pass}/>
				<button className="submitbutton" onClick={submit_params}>Generate Seed</button>
			</div>
		</div>
		<div className="generatorbox">
			{(phrase && seed) ? <SeedContainer phrase={phrase} seed={seed} m_xprv={m_xprv} m_xpub={m_xpub}/> : ''}
		</div>
	</div>);
}
