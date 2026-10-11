# Transitive private visibility probes — v1

Stage-only v61; v60 is already published. Reuse the existing immutable library sours-lat/R2Nsaa411cdaddab/1 (v58 source SHA d6afd2cab8dae06301bcef249685bcff2b3d986c144deda2c13e99094759fa45). It has private pick(float self) and exported forward(float x) using it internally.

Compile each source as a library, recording exact phase/message/location and source hash; no invalid library publication is required. Run the matching exported-forward library source as an access/compilation control. A library-access error settles neither question. If a private source compiles and can be published, record the immutable publication and execute a separate indicator importing it and plotting read(3.5), preserving every observer. Do not infer the capture result or message from TealScript.
