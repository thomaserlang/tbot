/*
	Copyright (c) 2013-2015, Fionn Kelleher All rights reserved.

	Redistribution and use in source and binary forms, with or without modification,
	are permitted provided that the following conditions are met:

		Redistributions of source code must retain the above copyright notice,
		this list of conditions and the following disclaimer.

		Redistributions in binary form must reproduce the above copyright notice,
		this list of conditions and the following disclaimer in the documentation and/or other materials
		provided with the distribution.

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
	ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
	IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
	INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
	(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
	OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
	WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
	ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
	OF SUCH DAMAGE.
*/

function parseComplexTag(tags, tagKey, splA = ",", splB = "/", splC) {
  const raw = tags[tagKey];

  if (raw === undefined) {
    return tags;
  }

  const tagIsString = typeof raw === "string";
  tags[`${tagKey}-raw`] = tagIsString ? raw : null;

  if (raw === true) {
    tags[tagKey] = null;
    return tags;
  }

  tags[tagKey] = {};

  if (tagIsString) {
    const spl = raw.split(splA);

    for (let i = 0; i < spl.length; i++) {
      const parts = spl[i].split(splB);
      let [, val] = parts;
      if (splC !== undefined && val) {
        val = val.split(splC);
      }
      if (parts[0]) tags[tagKey][parts[0]] = val || null;
    }
  }
  return tags;
}

export function parseTwitchBadges(msg) {
  return parseComplexTag(msg, "badges");
}

export function parseTwitchEmotes(msg) {
  return parseComplexTag(msg, "emotes", "/", ":", ",");
}
