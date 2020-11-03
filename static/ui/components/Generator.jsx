import React, { useState } from 'react';
import './sass/Generator.scss';

const ByteScheme = ({desc, bytes, active, updateSelected}) => {
	
	const byteclass = (bytes === active) ? "activebyte" : "bytes";

	const updateActivity = async () => {
		await updateSelected(bytes);
	}

	return (<div className={byteclass} onClick={updateActivity}>{desc}</div>);
}

const ByteSelector = ({selected, updateSelected}) => {
	
	// bytes of entropy/words in seed phrase - 16/12, 20/15, 24/18, 28/21, 32/24
	return (<div id="byteselector">
		<ByteScheme desc={"12 words"} bytes={16} active={selected} updateSelected={updateSelected}/>
		<ByteScheme desc={"15 words"} bytes={20} active={selected} updateSelected={updateSelected}/>
		<ByteScheme desc={"18 words"} bytes={24} active={selected} updateSelected={updateSelected}/>
		<ByteScheme desc={"21 words"} bytes={28} active={selected} updateSelected={updateSelected}/>
		<ByteScheme desc={"24 words"} bytes={32} active={selected} updateSelected={updateSelected}/>
	</div>);
}

const SeedContainer = ({phrase, seed}) => {
	return (<div className="seedcontainer">
		<div className="seedtext">Phrase:
		{phrase}
		</div>
		<div className="seedtext">Seed: 
		{seed}
		</div>
	</div>);
}

const Generator = () => {

	const [pass, updatePass] = useState('');
	const [retyped, updateRetyped] = useState('');
	const [selected, updateSelected] = useState(32);
	const [phrase, updatePhrase] = useState(null);
	const [seed, updateSeed] = useState(null);

	const update_pass = async (event) => {
		updatePass(event.target.value);
	}

	const update_retyped = async (event) => {
		updateRetyped(event.target.value);
	}

	const submit_params = async () => {
		if (pass != retyped) return;
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
	}

	return (<div className="generator">
		<ByteSelector selected={selected} updateSelected={updateSelected}/>
		<div className="passlabel">Passphrase</div>
		<input className="pass" id="passphrase" type="text" onChange={update_pass}/>
		<div className="passlabel">Retype Passphrase</div>
		<input className="pass" id="passphraseretyped" type="text" onChange={update_retyped}/>
		<button className="submitbutton" onClick={submit_params}>Generate Seed</button>
		{(phrase && seed) ? <SeedContainer phrase={phrase} seed={seed}/> : ''}
	</div>);
}

export {
	Generator
}
