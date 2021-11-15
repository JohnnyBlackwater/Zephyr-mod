# Python code obfuscated by www.development-tools.net 
 

import base64, codecs
magic = 'IyAtKi0gY29kaW5nOiB1dGYtOCAtKi0NCg0KJycnDQogICAgR2VuZXNpcyBBZGQtb24NCiAgICBDb3B5cmlnaHQgKEMpIDIwMTUgbGFtYmRhDQoNCiAgICAtTW9maWRpZWQgYnkgVGhlIENyZXcNCiAgICAtQ29weXJpZ2h0IChDKSAyMDE5IFRoZSBDcmV3DQoNCg0KICAgIFRoaXMgcHJvZ3JhbSBpcyBmcmVlIHNvZnR3YXJlOiB5b3UgY2FuIHJlZGlzdHJpYnV0ZSBpdCBhbmQvb3IgbW9kaWZ5DQogICAgaXQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBhcyBwdWJsaXNoZWQgYnkNCiAgICB0aGUgRnJlZSBTb2Z0d2FyZSBGb3VuZGF0aW9uLCBlaXRoZXIgdmVyc2lvbiAzIG9mIHRoZSBMaWNlbnNlLCBvcg0KICAgIChhdCB5b3VyIG9wdGlvbikgYW55IGxhdGVyIHZlcnNpb24uDQoNCiAgICBUaGlzIHByb2dyYW0gaXMgZGlzdHJpYnV0ZWQgaW4gdGhlIGhvcGUgdGhhdCBpdCB3aWxsIGJlIHVzZWZ1bCwNCiAgICBidXQgV0lUSE9VVCBBTlkgV0FSUkFOVFk7IHdpdGhvdXQgZXZlbiB0aGUgaW1wbGllZCB3YXJyYW50eSBvZg0KICAgIE1FUkNIQU5UQUJJTElUWSBvciBGSVRORVNTIEZPUiBBIFBBUlRJQ1VMQVIgUFVSUE9TRS4gIFNlZSB0aGUNCiAgICBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBmb3IgbW9yZSBkZXRhaWxzLg0KDQogICAgWW91IHNob3VsZCBoYXZlIHJlY2VpdmVkIGEgY29weSBvZiB0aGUgR05VIEdlbmVyYWwgUHVibGljIExpY2Vuc2UNCiAgICBhbG9uZyB3aXRoIHRoaXMgcHJvZ3JhbS4gIElmIG5vdCwgc2VlIDxodHRwOi8vd3d3LmdudS5vcmcvbGljZW5zZXMvPi4NCicnJw0KDQpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFic29sdXRlX2ltcG9ydCwgZGl2aXNpb24sIHByaW50X2Z1bmN0aW9uDQoNCmltcG9ydCByZSwgc3lzLCBnemlwLCB0aW1lLCByYW5kb20sIGJhc2U2NCwgdHJhY2ViYWNrDQoNCmltcG9ydCBzaW1wbGVqc29uIGFzIGpzb24NCg0KZnJvbSByZXNvdXJjZXMubGliLm1vZHVsZXMgaW1wb3J0IGNhY2hlLCBkb21fcGFyc2VyLCBsb2dfdXRpbHMsIGNvbnRyb2wsIGh1bnRlcg0KDQppbXBvcnQgc2l4DQpmcm9tIHNpeC5tb3ZlcyBpbXBvcnQgcmFuZ2UgYXMgeF9yYW5nZQ0KDQojIFB5Mg0KdHJ5Og0KICAgIGZyb20gdXJscGFyc2UgaW1wb3J0IHVybHBhcnNlLCB1cmxqb2luDQogICAgZnJvbSB1cmxsaWIgaW1wb3J0IHF1b3RlLCB1cmxlbmNvZGUsIHF1b3RlX3BsdXMsIGFkZGluZm91cmwNCiAgICBpbXBvcnQgY29va2llbGliDQogICAgaW1wb3J0IHVybGxpYjINCiAgICBmcm9tIGNTdHJpbmdJTyBpbXBvcnQgU3RyaW5nSU8NCiAgICBmcm9tIEhUTUxQYXJzZXIgaW1wb3J0IEhUTUxQYXJzZXINCiAgICB1bmVzY2FwZSA9IEhUTUxQYXJzZXIoKS51bmVzY2FwZQ0KICAgIEhUVFBFcnJvciA9IHVybGxpYjIuSFRUUEVycm9yDQoNCiMgUHkzOg0KZXhjZXB0IEltcG9ydEVycm9yOg0KICAgIGZyb20gaHR0cCBpbXBvcnQgY29va2llamFyIGFzIGNvb2tpZWxpYg0KICAgIGZyb20gaHRtbCBpbXBvcnQgdW5lc2NhcGUNCiAgICBpbXBvcnQgdXJsbGliLnJlcXVlc3QgYXMgdXJsbGliMg0KICAgIGZyb20gaW8gaW1wb3J0IFN0cmluZ0lPDQogICAgZnJvbSB1cmxsaWIucGFyc2UgaW1wb3J0IHVybHBhcnNlLCB1cmxqb2luLCBxdW90ZSwgdXJsZW5jb2RlLCBxdW90ZV9wbHVzDQogICAgZnJvbSB1cmxsaWIucmVzcG9uc2UgaW1wb3J0IGFkZGluZm91cmwNCiAgICBmcm9tIHVybGxpYi5lcnJvciBpbXBvcnQgSFRUUEVycm9yDQoNCmZpbmFsbHk6DQogICAgdXJsb3BlbiA9IHVybGxpYjIudXJsb3Blbg0KICAgIFJlcXVlc3QgPSB1cmxsaWIyLlJlcXVlc3QNCg0KaWYgc2l4LlBZMjoNCiAgICBfc3RyID0gc3RyDQogICAgc3RyID0gdW5pY29kZQ0KICAgIHVuaWNvZGUgPSB1bmljb2RlDQogICAgYmFzZXN0cmluZyA9IGJhc2VzdHJpbmcNCiAgICBkZWYgYnl0ZXMoYiwgZW5jb2Rpbmc9ImFzY2lpIik6DQogICAgICAgIHJldHVybiBfc3RyKGIpDQplbGlmIHNpeC5QWTM6DQogICAgYnl0ZXMgPSBieXRlcw0KICAgIHN0ciA9IHVuaWNvZGUgPSBiYXNlc3RyaW5nID0gc3RyDQoNCg0KDQpkZWYgcmVxdWVzdCh1cmwsIGNsb3NlPVRydWUsIHJlZGlyZWN0PVRydWUsIGVycm9yPUZhbHNlLCB2ZXJpZnk9VHJ1ZSwgcHJveHk9Tm9uZSwgcG9zdD1Ob25lLCBoZWFkZXJzPU5vbmUsIG1vYmlsZT1GYWxzZSwgWEhSPUZhbHNlLA0KICAgICAgICAgICAgbGltaXQ9Tm9uZSwgcmVmZXJlcj1Ob25lLGNvb2tpZT1Ob25lLCBjb21wcmVzc2lvbj1GYWxzZSwgb3V0cHV0PScnLCB0aW1lb3V0PSczMCcsIHVzZXJuYW1lPU5vbmUsIHBhc3N3b3JkPU5vbmUsIGFzX2J5dGVzPUZhbHNlKToNCg0KICAgICIiIg0KICAgIFJlLWFkYXB0ZWQgZnJvbSBUd2lsaWdodDAncyB0dWxpcCBtb2R1bGUgPT4gaHR0cHM6Ly9naXRodWIuY29tL1R3aWxpZ2h0MC9zY3JpcHQubW9kdWxlLnR1bGlwDQogICAgIiIiDQoNCiAgICB0cnk6DQogICAgICAgIHVybCA9IHNpeC5lbnN1cmVfdGV4dCh1cmwsIGVycm9ycz0naWdub3JlJykNCiAgICBleGNlcHQgRXhjZXB0aW9uOg0KICAgICAgICBwYXNzDQoNCiAgICBpZiBpc2luc3RhbmNlKHBvc3QsIGRpY3QpOg0KICAgICAgICBwb3N0ID0gYnl0ZXModXJsZW5jb2RlKHBvc3QpLCBlbmNvZGluZz0ndXRmLTgnKQ0KICAgIGVsaWYgaXNpbnN0YW5jZShwb3N0LCBzdHIpIGFuZCBzaXguUFkzOg0KICAgICAgICBwb3N0ID0gYnl0ZXMocG9zdCwgZW5jb2Rpbmc9J3V0Zi04JykNCg0KICAgIHRyeToNCiAgICAgICAgaGFuZGxlcnMgPSBbXQ0KDQogICAgICAgIGlmIHVzZXJuYW1lIGlzIG5vdCBOb25lIGFuZCBwYXNzd29yZCBpcyBub3QgTm9uZSBhbmQgbm90IHByb3h5Og0KDQogICAgICAgICAgICBwYXNzbWdyID0gdXJsbGliMi5IVFRQUGFzc3dvcmRNZ3JXaXRoRGVmYXVsdFJlYWxtKCkNCiAgICAgICAgICAgIHBhc3NtZ3IuYWRkX3Bhc3N3b3JkKE5vbmUsIHVyaT11cmwsIHVzZXI9dXNlcm5hbWUsIHBhc3N3ZD1wYXNzd29yZCkNCiAgICAgICAgICAgIGhhbmRsZXJzICs9IFt1cmxsaWIyLkhUVFBCYXNpY0F1dGhIYW5kbGVyKHBhc3NtZ3IpXQ0KICAgICAgICAgICAgb3BlbmVyID0gdXJsbGliMi5idWlsZF9vcGVuZXIoKmhhbmRsZXJzKQ0KICAgICAgICAgICAgdXJsbGliMi5pbnN0YWxsX29wZW5lcihvcGVuZXIpDQoNCiAgICAgICAgaWYgcHJveHkgaXMgbm90IE5vbmU6DQoNCiAgICAgICAgICAgIGlmIHVzZXJuYW1lIGlzIG5vdCBOb25lIGFuZCBwYXNzd29yZCBpcyBub3QgTm9uZToNCg0KICAgICAgICAgICAgICAgIGlmIHNpeC5QWTI6DQogICAgICAgICAgICAgICAgICAgIHBhc3NtZ3IgPSB1cmxsaWIyLlByb3h5QmFzaWNBdXRoSGFuZGxlcigpDQogICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgcGFzc21nciA9IHVybGxpYjIuSFRUUFBhc3N3b3JkTWdyKCkNCg0KICAgICAgICAgICAgICAgIHBhc3NtZ3IuYWRkX3Bhc3N3b3JkKE5vbmUsIHVyaT11cmwsIHVzZXI9dXNlcm5hbWUsIHBhc3N3ZD1wYXNzd29yZCkNCg0KICAgICAgICAgICAgICAgIGhhbmRsZXJzICs9IFsNCiAgICAgICAgICAgICAgICAgICAgdXJsbGliMi5Qcm94eUhhbmRsZXIoeydodHRwJzogJ3swfScuZm9ybWF0KHByb3h5KX0pLCB1cmxsaWIyLkhUVFBIYW5kbGVyLA0KICAgICAgICAgICAgICAgICAgICB1cmxsaWIyLlByb3h5QmFzaWNBdXRoSGFuZGxlcihwYXNzbWdyKQ0KICAgICAgICAgICAgICAgIF0NCiAgICAgICAgICAgIGVsc2U6DQogICAgICAgICAgICAgICAgaGFuZGxlcnMgKz0gW3VybGxpYjIuUHJveHlIYW5kbGVyKHsnaHR0cCc6J3swfScuZm9ybWF0KHByb3h5KX0pLCB1cmxsaWIyLkhUVFBIYW5kbGVyXQ0KICAgICAgICAgICAgb3BlbmVyID0gdXJsbGliMi5idWlsZF9vcGVuZXIoKmhhbmRsZXJzKQ0KICAgICAgICAgICAgdXJsbGliMi5pbnN0YWxsX29wZW5lcihvcGVuZXIpDQoNCiAgICAgICAgaWYgb3V0cHV0ID09ICdjb29raWUnIG9yIG91dHB1dCA9PSAnZXh0ZW5kZWQnIG9yIGNsb3NlIGlzIG5vdCBUcnVlOg0KDQogICAgICAgICAgICBjb29raWVzID0gY29va2llbGliLkxXUENvb2tpZUphcigpDQogICAgICAgICAgICBoYW5kbGVycyArPSBbdXJsbGliMi5IVFRQSGFuZGxlcigpLCB1cmxsaWIyLkhUVFBTSGFuZGxlcigpLCB1cmxsaWIyLkhUVFBDb29raWVQcm9jZXNzb3IoY29va2llcyldDQoNCiAgICAgICAgICAgIG9wZW5lciA9IHVybGxpYjIuYnVpbGRfb3BlbmVyKCpoYW5kbGVycykNCiAgICAgICAgICAgIHVybGxpYjIuaW5zdGFsbF9vcGVuZXIob3BlbmVyKQ0KDQogICAgICAgIHRyeToNCiAgICAgICAgICAgIGltcG9ydCBwbGF0Zm9ybQ0KICAgICAgICAgICAgaXNfWEJPWCA9IHBsYXRmb3JtLnVuYW1lKClbMV0gPT0gJ1hib3hPbmUnDQogICAgICAgIGV4Y2VwdCBFeGNlcHRpb246DQogICAgICAgICAgICBpc19YQk9YID0gRmFsc2UNCg0KICAgICAgICBpZiBub3QgdmVyaWZ5IGFuZCBzeXMudmVyc2lvbl9pbmZvID49ICgyLCA3LCAxMik6DQoNCiAgICAgICAgICAgIHRyeToNCg0KICAgICAgICAgICAgICAgIGltcG9ydCBzc2wNCiAgICAgICAgICAgICAgICBzc2xfY29udGV4dCA9IHNzbC5fY3JlYXRlX3VudmVyaWZpZWRfY29udGV4dCgpDQogICAgICAgICAgICAgICAgaGFuZGxlcnMgKz0gW3VybGxpYjIuSFRUUFNIYW5kbGVyKGNvbnRleHQ9c3NsX2NvbnRleHQpXQ0KICAgICAgICAgICAgICAgIG9wZW5lciA9IHVybGxpYjIuYnVpbGRfb3BlbmVyKCpoYW5kbGVycykNCiAgICAgICAgICAgICAgICB1cmxsaWIyLmluc3RhbGxfb3BlbmVyKG9wZW5lcikNCg0KICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbjoNCg0KICAgICAgICAgICAgICAgIHBhc3MNCg0KICAgICAgICBlbGlmIHZlcmlmeSBhbmQgKCgyLCA3LCA4KSA8IHN5cy52ZXJzaW9uX2luZm8gPCAoMiwgNywgMTIpIG9yIGlzX1hCT1gpOg0KDQogICAgICAgICAgICB0cnk6DQoNCiAgICAgICAgICAgICAgICBpbXBvcnQgc3NsDQogICAgICAgICAgICAgICAgdHJ5Og0KICAgICAgICAgICAgICAgICAgICBpbXBvcnQgX3NzbA0KICAgICAgICAgICAgICAgICAgICBDRVJUX05PTkUgPSBfc3NsLkNFUlRfTk9ORQ0KICAgICAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb246DQogICAgICAgICAgICAgICAgICAgIENFUlRfTk9ORSA9IHNzbC5DRVJUX05PTkUNCiAgICAgICAgICAgICAgICBzc2xfY29udGV4dCA9IHNzbC5jcmVhdGVfZGVmYXVsdF9jb250ZXh0KCkNCiAgICAgICAgICAgICAgICBzc2xfY29udGV4dC5jaGVja19ob3N0bmFtZSA9IEZhbHNlDQogICAgICAgICAgICAgICAgc3NsX2NvbnRleHQudmVyaWZ5X21vZGUgPSBDRVJUX05PTkUNCiAgICAgICAgICAgICAgICBoYW5kbGVycyArPSBbdXJsbGliMi5IVFRQU0hhbmRsZXIoY29udGV4dD1zc2xfY29udGV4dCldDQogICAgICAgICAgICAgICAgb3BlbmVyID0gdXJsbGliMi5idWlsZF9vcGVuZXIoKmhhbmRsZXJzKQ0KICAgICAgICAgICAgICAgIHVybGxpYjIuaW5zdGFsbF9vcGVuZXIob3BlbmVyKQ0KDQogICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uOg0KDQogICAgICAgICAgICAgICAgcGFzcw0KDQogICAgICAgIHRyeToNCiAgICAgICAgICAgIGhlYWRlcnMudXBkYXRlKGhlYWRlcnMpDQogICAgICAgIGV4Y2VwdCBFeGNlcHRpb246DQogICAgICAgICAgICBoZWFkZXJzID0ge30NCg0KICAgICAgICBpZiAnVXNlci1BZ2VudCcgaW4gaGVhZGVyczoNCiAgICAgICAgICAgIHBhc3MNCiAgICAgICAgZWxpZiBtb2JpbGUgaXMgbm90IFRydWU6DQogICAgICAgICAgICAjaGVhZGVyc1snVXNlci1BZ2VudCddID0gYWdlbnQoKQ0KICAgICAgICAgICAgaGVhZGVyc1snVXNlci1BZ2VudCddID0gY2FjaGUuZ2V0KHJhbmRvbWFnZW50LCAxMikNCiAgICAgICAgZWxzZToNCiAgICAgICAgICAgIGhlYWRlcnNbJ1VzZXItQWdlbnQnXSA9IGNhY2hlLmdldChyYW5kb21tb2JpbGVhZ2VudCwgMTIpDQoNCiAgICAgICAgaWYgJ1JlZmVyZXInIGluIGhlYWRlcnM6DQogICAgICAgICAgICBwYXNzDQogICAgICAgIGVsaWYgcmVmZXJlciBpcyBOb25lOg0KICAgICAgICAgICAgaGVhZGVyc1snUmVmZXJlciddID0gJyVzOi8vJXMvJyAlICh1cmxwYXJzZSh1cmwpLnNjaGVtZSwgdXJscGFyc2UodXJsKS5uZXRsb2MpDQogICAgICAgIGVsc2U6DQogICAgICAgICAgICBoZWFkZXJzWydSZWZlcmVyJ10gPSByZWZlcmVyDQoNCiAgICAgICAgaWYgbm90ICdBY2NlcHQtTGFuZ3VhZ2UnIGluIGhlYWRlcnM6DQogICAgICAgICAgICBoZWFkZXJzWydBY2NlcHQtTGFuZ3VhZ2UnXSA9ICdlbi1VUycNCg0KICAgICAgICBpZiAnWC1SZXF1ZXN0ZWQtV2l0aCcgaW4gaGVhZGVyczoNCiAgICAgICAgICAgIHBhc3MNCiAgICAgICAgZWxpZiBYSFIgaXMgVHJ1ZToNCiAgICAgICAgICAgIGhlYWRlcnNbJ1gtUmVxdWVzdGVkLVdpdGgnXSA9ICdYTUxIdHRwUmVxdWVzdCcNCg0KICAgICAgICBpZiAnQ29va2llJyBpbiBoZWFkZXJzOg0KICAgICAgICAgICAgcGFzcw0KICAgICAgICBlbGlmIGNvb2tpZSBpcyBub3QgTm9uZToNCiAgICAgICAgICAgIGhlYWRlcnNbJ0Nvb2tpZSddID0gY29va2llDQoNCiAgICAgICAgaWYgJ0FjY2VwdC1FbmNvZGluZycgaW4gaGVhZGVyczoNCiAgICAgICAgICAgIHBhc3MNCiAgICAgICAgZWxpZiBjb21wcmVzc2lvbiBhbmQgbGltaXQgaXMgTm9uZToNCiAgICAgICAgICAgIGhlYWRlcnNbJ0FjY2VwdC1FbmNvZGluZyddID0gJ2d6aXAnDQoNCiAgICAgICAgaWYgcmVkaXJlY3QgaXMgRmFsc2U6DQoNCiAgICAgICAgICAgIGNsYXNzIE5vUmVkaXJlY3RIYW5kbGVyKHVybGxpYjIuSFRUUFJlZGlyZWN0SGFuZGxlcik6DQoNCiAgICAgICAgICAgICAgICBkZWYgaHR0cF9lcnJvcl8zMDIoc2VsZiwgcmVxc3QsIGZwLCBjb2RlLCBtc2csIGhlYWQpOg0KDQogICAgICAgICAgICAgICAgICAgIGluZm91cmwgPSBhZGRpbmZvdXJsKGZwLCBoZWFkLCByZXFzdC5nZXRfZnVsbF91cmwoKSkNCiAgICAgICAgICAgICAgICAgICAgaW5mb3VybC5zdGF0dXMgPSBjb2RlDQogICAgICAgICAgICAgICAgICAgIGluZm91cmwuY29kZSA9IGNvZGUNCg0KICAgICAgICAgICAgICAgICAgICByZ'
love = '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'
god = 'VyLnBhcnNlX2RvbShodG1sLCBuYW1lLCBhdHRycywgcmV0KQ0KDQogICAgaWYgcmV0Og0KICAgICAgICByZXN1bHRzID0gW3Jlc3VsdC5hdHRyc1tyZXQubG93ZXIoKV0gZm9yIHJlc3VsdCBpbiByZXN1bHRzXQ0KICAgIGVsc2U6DQogICAgICAgIHJlc3VsdHMgPSBbcmVzdWx0LmNvbnRlbnQgZm9yIHJlc3VsdCBpbiByZXN1bHRzXQ0KDQogICAgcmV0dXJuIHJlc3VsdHMNCg0KDQpkZWYgcmVwbGFjZUhUTUxDb2Rlcyh0eHQpOg0KICAgIHR4dCA9IHJlLnN1YigiKCYjWzAtOV0rKShbXjteMC05XSspIiwgIlxcMTtcXDIiLCB0eHQpDQogICAgdHh0ID0gdW5lc2NhcGUodHh0KQ0KICAgIHR4dCA9IHR4dC5yZXBsYWNlKCImcXVvdDsiLCAiXCIiKQ0KICAgIHR4dCA9IHR4dC5yZXBsYWNlKCImYW1wOyIsICImIikNCiAgICB0eHQgPSB0eHQucmVwbGFjZSgiJmx0OyIsICI8IikNCiAgICB0eHQgPSB0eHQucmVwbGFjZSgiJmd0OyIsICI+IikNCiAgICB0eHQgPSB0eHQucmVwbGFjZSgiJiMzODsiLCAiJiIpDQogICAgdHh0ID0gdHh0LnJlcGxhY2UoIiZuYnNwOyIsICIiKQ0KICAgIHR4dCA9IHR4dC5yZXBsYWNlKCcmIzgyMzA7JywgJy4uLicpDQogICAgdHh0ID0gdHh0LnJlcGxhY2UoJyYjODIxNzsnLCAnXCcnKQ0KICAgIHR4dCA9IHR4dC5yZXBsYWNlKCcmIzgyMTE7JywgJy0nKQ0KICAgIHR4dCA9IHR4dC5zdHJpcCgpDQogICAgcmV0dXJuIHR4dA0KDQoNCmRlZiByYW5kb21hZ2VudCgpOg0KICAgIEJSX1ZFUlMgPSBbDQogICAgICAgIFsnJXMuMCcgJSBpIGZvciBpIGluIHhfcmFuZ2UoMTgsIDUwKV0sDQogICAgICAgIFsnMzcuMC4yMDYyLjEwMycsICczNy4wLjIwNjIuMTIwJywgJzM3LjAuMjA2Mi4xMjQnLCAnMzguMC4yMTI1LjEwMScsICczOC4wLjIxMjUuMTA0JywgJzM4LjAuMjEyNS4xMTEnLA0KICAgICAgICAgJzM5LjAuMjE3MS43MScsICczOS4wLjIxNzEuOTUnLCAnMzkuMC4yMTcxLjk5JywgJzQwLjAuMjIxNC45MycsICc0MC4wLjIyMTQuMTExJywgJzQwLjAuMjIxNC4xMTUnLA0KICAgICAgICAgJzQyLjAuMjMxMS45MCcsICc0Mi4wLjIzMTEuMTM1JywgJzQyLjAuMjMxMS4xNTInLCAnNDMuMC4yMzU3LjgxJywgJzQzLjAuMjM1Ny4xMjQnLCAnNDQuMC4yNDAzLjE1NScsDQogICAgICAgICAnNDQuMC4yNDAzLjE1NycsICc0NS4wLjI0NTQuMTAxJywgJzQ1LjAuMjQ1NC44NScsICc0Ni4wLjI0OTAuNzEnLCAnNDYuMC4yNDkwLjgwJywgJzQ2LjAuMjQ5MC44NicsDQogICAgICAgICAnNDcuMC4yNTI2LjczJywgJzQ3LjAuMjUyNi44MCcsICc0OC4wLjI1NjQuMTE2JywgJzQ5LjAuMjYyMy4xMTInLCAnNTAuMC4yNjYxLjg2JywgJzUxLjAuMjcwNC4xMDMnLA0KICAgICAgICAgJzUyLjAuMjc0My4xMTYnLCAnNTMuMC4yNzg1LjE0MycsICc1NC4wLjI4NDAuNzEnLCAnNjEuMC4zMTYzLjEwMCddLA0KICAgICAgICBbJzExLjAnXSwNCiAgICAgICAgWyc4LjAnLCAnOS4wJywgJzEwLjAnLCAnMTAuNiddXQ0KICAgIFdJTl9WRVJTID0gWydXaW5kb3dzIE5UIDEwLjAnLCAnV2luZG93cyBOVCA3LjAnLCAnV2luZG93cyBOVCA2LjMnLCAnV2luZG93cyBOVCA2LjInLA0KICAgICAgICAgICAgICAgICdXaW5kb3dzIE5UIDYuMScsICdXaW5kb3dzIE5UIDYuMCcsICdXaW5kb3dzIE5UIDUuMScsICdXaW5kb3dzIE5UIDUuMCddDQogICAgRkVBVFVSRVMgPSBbJzsgV09XNjQnLCAnOyBXaW42NDsgSUE2NCcsICc7IFdpbjY0OyB4NjQnLCAnJ10NCiAgICBSQU5EX1VBUyA9IFsnTW96aWxsYS81LjAgKHt3aW5fdmVyfXtmZWF0dXJlfTsgcnY6e2JyX3Zlcn0pIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gve2JyX3Zlcn0nLA0KICAgICAgICAgICAgICAgICdNb3ppbGxhLzUuMCAoe3dpbl92ZXJ9e2ZlYXR1cmV9KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUve2JyX3Zlcn0gU2FmYXJpLzUzNy4zNicsDQogICAgICAgICAgICAgICAgJ01vemlsbGEvNS4wICh7d2luX3Zlcn17ZmVhdHVyZX07IFRyaWRlbnQvNy4wOyBydjp7YnJfdmVyfSkgbGlrZSBHZWNrbycsDQogICAgICAgICAgICAgICAgJ01vemlsbGEvNS4wIChjb21wYXRpYmxlOyBNU0lFIHticl92ZXJ9OyB7d2luX3Zlcn17ZmVhdHVyZX07IFRyaWRlbnQvNi4wKSddDQogICAgaW5kZXggPSByYW5kb20ucmFuZHJhbmdlKGxlbihSQU5EX1VBUykpDQogICAgcmV0dXJuIFJBTkRfVUFTW2luZGV4XS5mb3JtYXQoDQogICAgICAgIHdpbl92ZXI9cmFuZG9tLmNob2ljZShXSU5fVkVSUyksDQogICAgICAgIGZlYXR1cmU9cmFuZG9tLmNob2ljZShGRUFUVVJFUyksDQogICAgICAgIGJyX3Zlcj1yYW5kb20uY2hvaWNlKEJSX1ZFUlNbaW5kZXhdKSkNCg0KDQpkZWYgcmFuZG9tbW9iaWxlYWdlbnQobW9iaWxlKToNCiAgICBfbW9iYWdlbnRzID0gWw0KICAgICAgICAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDcuMTsgdml2byAxNzE2IEJ1aWxkL04yRzQ3SCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYxLjAuMzE2My45OCBNb2JpbGUgU2FmYXJpLzUzNy4zNicsDQogICAgICAgICdNb3ppbGxhLzUuMCAoTGludXg7IFU7IEFuZHJvaWQgNi4wLjE7IHpoLUNOOyBGNTEyMSBCdWlsZC8zNC4wLkEuMS4yNDcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS80MC4wLjIyMTQuODkgVUNCcm93c2VyLzExLjUuMS45NDQgTW9iaWxlIFNhZmFyaS81MzcuMzYnLA0KICAgICAgICAnTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDcuMDsgU0FNU1VORyBTTS1OOTIwQyBCdWlsZC9OUkQ5ME0pIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFNhbXN1bmdCcm93c2VyLzYuMiBDaHJvbWUvNTYuMC4yOTI0Ljg3IE1vYmlsZSBTYWZhcmkvNTM3LjM2JywNCiAgICAgICAgJ01vemlsbGEvNS4wIChpUGhvbmU7IENQVSBpUGhvbmUgT1MgMTJfMSBsaWtlIE1hYyBPUyBYKSBBcHBsZVdlYktpdC82MDUuMS4xNSAoS0hUTUwsIGxpa2UgR2Vja28pIENyaU9TLzgwLjAuMzk4Ny45NSBNb2JpbGUvMTVFMTQ4IFNhZmFyaS82MDUuMScsDQogICAgICAgICdNb3ppbGxhLzUuMCAoaVBhZDsgQ1BVIE9TIDEwXzJfMSBsaWtlIE1hYyBPUyBYKSBBcHBsZVdlYktpdC82MDIuNC42IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xMC4wIE1vYmlsZS8xNEQyNyBTYWZhcmkvNjAyLjEnXQ0KDQogICAgaWYgbW9iaWxlID09ICdhbmRyb2lkJzoNCiAgICAgICAgcmV0dXJuIHJhbmRvbS5jaG9pY2UoX21vYmFnZW50c1s6M10pDQogICAgZWxzZToNCiAgICAgICAgcmV0dXJuIHJhbmRvbS5jaG9pY2UoX21vYmFnZW50c1szOjVdKQ0KDQoNCmRlZiBhZ2VudCgpOg0KICAgIHJldHVybiByYW5kb20uY2hvaWNlKA0KICAgICAgICAgICAgWyJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvODAuMC4zOTg3LjE0OSBTYWZhcmkvNTM3LjM2IiwNCiAgICAgICAgICAgICJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xM182KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvODAuMC4zOTg3LjE0OSBTYWZhcmkvNTM3LjM2IiwNCiAgICAgICAgICAgICJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84MC4wLjM5ODcuMTQ5IFNhZmFyaS81MzcuMzYiLA0KICAgICAgICAgICAgIk1vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA4LjAuMDspIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84MC4wLjM5ODcuMTQ5IE1vYmlsZSBTYWZhcmkvNTM3LjM2IiwNCiAgICAgICAgICAgICJNb3ppbGxhLzUuMCAoaVBob25lOyBDUFUgaVBob25lIE9TIDEyXzEgbGlrZSBNYWMgT1MgWCkgQXBwbGVXZWJLaXQvNjA1LjEuMTUgKEtIVE1MLCBsaWtlIEdlY2tvKSBDcmlPUy84MC4wLjM5ODcuOTUgTW9iaWxlLzE1RTE0OCBTYWZhcmkvNjA1LjEiLA0KICAgICAgICAgICAgIk1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDYuMTsgV09XNjQ7IHJ2OjU0LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvNzQuMCIsDQogICAgICAgICAgICAiTW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTAuMTM7IHJ2OjYxLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvNzQuMCIsDQogICAgICAgICAgICAiTW96aWxsYS81LjAgKFgxMTsgTGludXggaTU4NjsgcnY6MzEuMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC83NC4wIiwNCiAgICAgICAgICAgICJNb3ppbGxhLzUuMCAoQW5kcm9pZCA4LjAuMDsgTW9iaWxlOyBydjo2MS4wKSBHZWNrby82MS4wIEZpcmVmb3gvNjguMCIsDQogICAgICAgICAgICAiTW96aWxsYS81LjAgKGlQaG9uZTsgQ1BVIGlQaG9uZSBPUyAxMl8xIGxpa2UgTWFjIE9TIFgpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgRnhpT1MvMjQuMCBNb2JpbGUvMTZCOTIgU2FmYXJpLzYwNS4xLjE1IiwNCiAgICAgICAgICAgICJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xNV80KSBBcHBsZVdlYktpdC82MDUuMS4xNSAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vMTMuMSBTYWZhcmkvNjA1LjEuMTUiLA0KICAgICAgICAgICAgIk1vemlsbGEvNS4wIChpUGhvbmU7IENQVSBpUGhvbmUgT1MgMTNfNCBsaWtlIE1hYyBPUyBYKSBBcHBsZVdlYktpdC82MDUuMS4xNSAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vMTMuMSBNb2JpbGUvMTVFMTQ4IFNhZmFyaS82MDQuMSIsDQogICAgICAgICAgICAiTW96aWxsYS81LjAgKGlQYWQ7IENQVSBPUyAxM180IGxpa2UgTWFjIE9TIFgpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xMy4xIE1vYmlsZS8xNUUxNDggU2FmYXJpLzYwNC4xIiwNCiAgICAgICAgICAgICJNb3ppbGxhLzUuMCAoaVBvZCBUb3VjaDsgQ1BVIGlQaG9uZSBPUyAxM180IGxpa2UgTWFjIE9TIFgpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xMy4xIE1vYmlsZS8xNUUxNDggU2FmYXJpLzYwNC4xIiwNCiAgICAgICAgICAgICJNb3ppbGxhLzQuMCAoY29tcGF0aWJsZTsgTVNJRSA4LjA7IFdpbmRvd3MgTlQgNS4xOyBUcmlkZW50LzQuMCkiLA0KICAgICAgICAgICAgIk1vemlsbGEvNC4wIChjb21wYXRpYmxlOyBNU0lFIDcuMDsgV2luZG93cyBOVCA2LjA7IFdPVzY0OyBUcmlkZW50LzQuMDspIiwNCiAgICAgICAgICAgICJNb3ppbGxhLzQuMCAoY29tcGF0aWJsZTsgTVNJRSA4LjA7IFdpbmRvd3MgTlQgNi4xOyBUcmlkZW50LzQuMCkiLA0KICAgICAgICAgICAgIk1vemlsbGEvNC4wIChjb21wYXRpYmxlOyBNU0lFIDkuMDsgV2luZG93cyBOVCA2LjApIiwNCiAgICAgICAgICAgICJNb3ppbGxhLzQuMCAoY29tcGF0aWJsZTsgTVNJRSA5LjA7IFdpbmRvd3MgTlQgNi4xKSIsDQogICAgICAgICAgICAiTW96aWxsYS81LjAgKGNvbXBhdGlibGU7IE1TSUUgMTAuMDsgV2luZG93cyBOVCA2LjE7IFdPVzY0OyBUcmlkZW50LzYuMCkiLA0KICAgICAgICAgICAgIk1vemlsbGEvNS4wIChjb21wYXRpYmxlOyBNU0lFIDEwLjA7IFdpbmRvd3MgTlQgNi4yKSIsDQogICAgICAgICAgICAiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4xOyBUcmlkZW50LzcuMDsgcnY6MTEuMCkgbGlrZSBHZWNrbyIsDQogICAgICAgICAgICAiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4yOyBUcmlkZW50LzcuMDsgcnY6MTEuMCkgbGlrZSBHZWNrbyIsDQogICAgICAgICAgICAiV2luZG93cyA4LjEJTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4zOyBUcmlkZW50LzcuMDsgcnY6MTEuMCkgbGlrZSBHZWNrbyIsDQogICAgICAgICAgICAiV2luZG93cyAxMAlNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBUcmlkZW50LzcuMDsgcnY6MTEuMCkgbGlrZSBHZWNrbyIsDQogICAgICAgICAgICAiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzgwLjAuMzk4Ny4xNDkgU2FmYXJpLzUzNy4zNiBFZGcvODAuMC4zNjEuNjkiLA0KICAgICAgICAgICAgIk1vemlsbGEvNS4wIChXaW5kb3dzIE1vYmlsZSAxMDsgQW5kcm9pZCA4LjAuMDsgTWljcm9zb2Z0OyBMdW1pYSA5NTBYTCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzgwLjAuMzk4Ny4xNDkgTW9iaWxlIFNhZmFyaS81MzcuMzYgRWRnZS84MC4wLjM2MS42OSIsDQogICAgICAgICAgICAiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NDsgWGJveDsgWGJveCBPbmUpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84MC4wLjM5ODcuMTQ5IFNhZmFyaS81MzcuMzYgRWRnZS80NC4xODM2My44MTMxIiwNCiAgICAgICAgICAgICJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvODAuMC4zOTg3LjE0OSBTYWZhcmkvNTM3LjM2IE9QUi82Ny4wLjM1NzUuMTE1IiwNCiAgICAgICAgICAgICJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xNF81KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvODAuMC4zOTg3LjE0OSBTYWZhcmkvNTM3LjM2IE9QUi82Ny4wLjM1NzUuMTE1IiwNCiAgICAgICAgICAgICJNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84MC4wLjM5ODcuMTQ5IFNhZmFyaS81MzcuMzYgT1BSLzY3LjAuMzU3NS4xMTUiLA0KICAgICAgICAgICAgIk1vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA5OyBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvODAuMC4zOTg3LjE0OSBNb2JpbGUgU2F'
destiny = 'zLKWcYmHmAl4mAvOCHSViAGHhZv4lAmR5Vy0cQDbAPzEyMvO0nJ55qFu1pzjcBt0XVPNtVUHtCFOlMKS1MKA0XUIloPxAPvNtVPOyVQ0tpzHhL29gpTyfMFtaMTIwo2EyYvb/VvuoKvWqXvxvYPuoKvkqXvxfVvuoKvWqXvxvYPuoKvkqXvxfXSgrYS0dXFjbJ15pXI0dXFpcYzMcozEuoTjbqFyoZS0APvNtVPOzVQ0tnUIhqTIlYzu1oaEypvuyJmOqYPOcoaDbMIfkKFxfVTIoZy0fVTyhqPuyJmAqXFjtnJ50XTIoAS0cYPOcoaDbMIf1KFxcQDbtVPNtMlN9VUWyYzMcozEuoTjbpvqpYzS0qUWpXSjvnUWyMyjvYSjvXP4eClypVvpfVTLcJmSqQDbtVPNtMlN9VTphpzIjoTSwMFtaVPpfWlHlZPpcQDbtVPNtpzI0qKWhVTpAPt0XQDcwoTSmplOQMzAio2gcMGbAPvNtVPOxMJLtK19cozy0K18bp2IfMvx6QDbtVPNtVPNtVUAyoTLhL29in2yyVQ0tGz9hMD0XQDbtVPNtMTIzVTqyqPumMJkzYPOhMKEfo2ZfVUIuYPO0nJ1yo3I0XGbAPvNtVPNtVPNtqUW5Bt0XVPNtVPNtVPNtVPNtp2IfMv5hMKEfo2ZtCFOhMKEfo2ZAPvNtVPNtVPNtVPNtVUAyoTLhqJRtCFO1LD0XVPNtVPNtVPNtVPNtp2IfMv50nJ1yo3I0VQ0tqTygMJ91qN0XVPNtVPNtVPNtVPNtp2IfMv5wo29enJHtCFOBo25yQDbtVPNtVPNtVPNtVPOmMJkzYy9aMKEsL29in2yyXT5yqTkiLljtqJRfVUEcoJIiqKDcQDbtVPNtVPNtVPNtVPOcMvOmMJkzYzAio2gcMFOcplOBo25yBt0XVPNtVPNtVPNtVPNtVPNtVTkiM191qTyfpl5fo2pbWlImVUWyqUIlozIxVTShVTIlpz9lYvOQo3IfMPOho3DtL29foTIwqPO0o2gyoaZhWlNyVT5yqTkiLljtoT9aK3I0nJkmYxkCE0ESDyIUXD0XVPNtVPNtVPNtVPNtpzI0qKWhVUAyoTLhL29in2yyQDbtVPNtVPNtVTI4L2IjqPOSrTAypUEco24tLKZtMGbAPvNtVPNtVPNtVPNtVTkiM191qTyfpl5fo2pbWlImVUWyqUIlozIxVTShVTIlpz9lYvOQo3IfMPOho3DtL29foTIwqPO0o2gyoaZtYFOSpaWipwbtWKZhWlNyVPuhMKEfo2ZfVUA0pvuyXFxfQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTkiM191qTyfpl5ZG0qREHWIElxAPvNtVPNtVPNtVPNtVUWyqUIlovOmMJkzYzAio2gcMD0XQDbtVPNtMTIzVS9aMKEsL29in2yyXUAyoTLfVT5yqTkiLljtqJRfVUEcoJIiqKDcBt0XVPNtVPNtVPOwoTSmplOBo1WyMTylMJA0nJ9hXUIloTkcLwVhFSEHHRIlpz9lHUWiL2Imp29lXGbAPvNtVPNtVPNtVPNtVTEyMvObqUEjK3Wyp3OioaAyXUAyoTLfVUWypKIyp3DfVUWyp3OioaAyXGbAPvNtVPNtVPNtVPNtVPNtVPOlMKE1pz4tpzImpT9hp2HAPt0XVPNtVPNtVPOxMJLtpTSlp2IXH1A0pzyhMlumXGbAPvNtVPNtVPNtVPNtVUElrGbAPvNtVPNtVPNtVPNtVPNtVPOiMzMmMKDtCFNkVTyzVUAoZS0tCG0tWlfaVTIfp2HtZN0XVPNtVPNtVPNtVPNtVPNtVUMuoPN9VTyhqPtAPvNtVPNtVPNtVPNtVPNtVPNtVPNtMKMuoPumYaWypTkuL2HbWlReJ10aYPNaZFpcYaWypTkuL2HbWlRuJ10aYPNaZFpcYaWypTkuL2HbW1gqWljtWmNaXF5lMKOfLJAyXPpbWljtW3A0pvtaXIgiMzMmMKD6KFxcQDbtVPNtVPNtVPNtVPNtVPNtpzI0qKWhVUMuoN0XVPNtVPNtVPNtVPNtMKuwMKO0Bt0XVPNtVPNtVPNtVPNtVPNtVUOup3ZAPt0XVPNtVPNtVPOwo29enJImVQ0tL29in2yyoTyvYxkKHRAio2gcMHcupvtcQDbtVPNtVPNtVT9jMJ5ypvN9VUIloTkcLwVhLaIcoTEso3OyozIlXR5iHzIxnKWyL3Eco24fVUIloTkcLwVhFSEHHRAio2gcMIOlo2Ayp3Aipvuwo29enJImXFxAPvNtVPNtVPNto3OyozIlYzSxMTuyLJEypaZtCFOoXPqIp2IlYHSaMJ50WljtqJRcKD0XVPNtVPNtVPO0pax6QDbtVPNtVPNtVPNtVPOlMKAjo25mMFN9VT9jMJ5ypv5ipTIhXT5yqTkiLljtqTygMJ91qQ1coaDbqTygMJ91qPxcQDbtVPNtVPNtVPNtVPOlMKA1oUDtCFOlMKAjo25mMF5lMJSxXPxAPvNtVPNtVPNtMKuwMKO0VRuHISOSpaWipvOuplOlMKAjo25mMGbAPvNtVPNtVPNtVPNtVUWyp3IfqPN9VUWyp3OioaAyYaWyLJDbXD0XVPNtVPNtVPNtVPNtqUW5Bt0XVPNtVPNtVPNtVPNtVPNtVTIhL29xnJ5aVQ0tpzImpT9hp2HhnJ5zoltcYzqyqTuyLJEypvtaD29hqTIhqP1SozAiMTyhMlpcQDbtVPNtVPNtVPNtVPOyrTAypUD6QDbtVPNtVPNtVPNtVPNtVPNtMJ5wo2EcozptCFOBo25yQDbtVPNtVPNtVPNtVPOcMvOyozAiMTyhMlN9CFNaM3ccpPp6QDbtVPNtVPNtVPNtVPNtVPNtpzImqJk0VQ0tM3ccpP5UrzyjEzyfMFuznJkyo2WdCIA0pzyhM0yCXUWyp3IfqPxcYaWyLJDbXD0XQDbtVPNtVPNtVTcmL2ufVQ0tpzHhL29gpTyfMFtaozSgMG0vnaAwnTksqzZvVUMuoUIyCFVbYvf/XFViCvpcYzMcozEuoTjbpzImqJk0XIfjKD0XVPNtVPNtVPOcozy0VQ0tpzHhL29gpTyfMFtap2I0ITygMJ91qSjbMaIhL3Eco25pXSjcr1kmXv4dCl4dBvthXw8csGfaXF5znJ5xLJkfXUWyp3IfqPyoZS0APvNtVPNtVPNtLaIcoTEypvN9VUWyYzAioKOcoTHbpvWwnTSfoTIhM2HgMz9loIjaKPx7KUZdXP4dXJRhqvVcYzMcozEuoTjbpzImqJk0XIfjKD0XQDbtVPNtVPNtVTyzVPpiWlOcovOcozy0Bt0XVPNtVPNtVPNtVPNtnJ5cqPN9VTyhnKDhp3OfnKDbWl8aXD0XVPNtVPNtVPNtVPNtMTIwpayjqSMuoPN9VUOupaAyFyAGqUWcozpbnJ5cqSfjKFxtYlOzoT9uqPujLKWmMHcGH3ElnJ5aXTyhnKEoZI0cXD0XVPNtVPNtVPOyoUAyBt0XVPNtVPNtVPNtVPNtMTIwpayjqSMuoPN9VUOupaAyFyAGqUWcozpbnJ5cqPxAPt0XVPNtVPNtVPOfnJ5yplN9VTW1nJkxMKVhp3OfnKDbWmfaXD0XVPNtVPNtVPOzo3VtoTyhMFOcovOfnJ5ypmbAPvNtVPNtVPNtVPNtVTyzVTkyovufnJ5yXFN+VQNtLJ5xVPp9WlOcovOfnJ5yBt0XVPNtVPNtVPNtVPNtVPNtVUAyL3Eco25mVQ0toTyhMF5mpTkcqPtaCFpcQDbtVPNtVPNtVPNtVPNtVPNtnJLtWl8aVTyhVUAyL3Eco25mJmSqBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPOmqJWmMJAmVQ0tp2IwqTyioaAoZI0hp3OfnKDbWl8aXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPOfnJ5yK3MuoPN9VUOupaAyFyAGqUWcozpbp3Ivp2Iwp1fjKFxtYlOzoT9uqPujLKWmMHcGH3ElnJ5aXUA1LaAyL3AoZI0cXD0XVPNtVPNtVPNtVPNtVPNtVTIfp2H6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVTkcozIsqzSfVQ0tpTSlp2IXH1A0pzyhMlumMJA0nJ9hp1fkKFxAPvNtVPNtVPNtVPNtVPNtVPOxMJAlrKO0IzSfVQ0tMzkiLKDbMKMuoPtaWF4kAzLaVPHtMTIwpayjqSMuoPNeVUAyL3Eco25mJmOqJl0kKFNeVPpyYwR2MvptWFOfnJ5yK3MuoPxcQDbAPvNtVPNtVPNtLJ5mq2IlVQ0tMzkiLKDbWlHhZGOzWlNyVTEyL3W5pUEJLJjcVPftoTIhXUIloUOupaAyXT5yqTkiLlxhozI0oT9wXD0XQDbtVPNtVPNtVUS1MKW5VQ0tWlImL2EhYJAanF9fY2Abn19dp2AboQ9dp2AboS92Lm0yplMdp2AboS9uoaA3MKV9WKZaVPHtXT5yqTkiLljtnaAwnTjfVTShp3qypvxAPt0XVPNtVPNtVPOcMvNaqUyjMG0vnTyxMTIhVvOhLJ1yCFWjLKAmVvptnJ4tpzImqJk0Bt0XVPNtVPNtVPNtVPNtpTSmp3MuoPN9VUWyYzMcozEuoTjbW25uoJH9VaOup3ZvVUMuoUIyCFVbYvb/XFVaYPOlMKA1oUDcJmOqQDbtVPNtVPNtVPNtVPOkqJIlrFN9VPpyp2Axov1wM2xioP9wnTgsnaAwnTj/pTSmpm0yplMdp2AboS92Lm0yplMdp2AboS9uoaA3MKV9WKZaVPHtXN0XVPNtVPNtVPNtVPNtVPNtVT5yqTkiLljtpKIiqTIspTk1plujLKAmqzSfXFjtnaAwnTjfVTShp3qypvxAPvNtVPNtVPNtVPNtVUEcoJHhp2kyMKNbAvxAPt0XVPNtVPNtVPOipTIhMKVhLJExnTIuMTIlplN9VSfbW1ImMKVgDJqyoaDaYPO1LFxfQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPtaHzIzMKWypvpfVT5yqTkiLlxfQDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPtaDJAwMKO0WljtW3EyrUDinUEgoPjtLKOjoTywLKEco24irTu0oJjerT1fYPOupUOfnJAuqTyiov94oJjfVPbiXvpcYN0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNbW0SwL2IjqP1SozAiMTyhMlpfVPqarzyjYPOxMJMfLKEyWlyqQDbAPvNtVPNtVPNtpzImpT9hp2HtCFOipTIhMKVho3OyovukqJIlrFxAPvNtVPNtVPNtpzImpT9hp2HhL2kip2HbXD0XQDbtVPNtVPNtVTAio2gcMFN9VPp7VPphnz9covuoWlImCFImWlNyVPucYz5uoJHfVTxhqzSfqJHcVTMipvOcVTyhVTAio2gcMKAqXD0XVPNtVPNtVPOcMvNaL2MsL2kyLKWuozAyWlOcovOwo29enJH6VUAyoTLhL29in2yyVQ0tL29in2yyQDbAPt0XL2kup3ZtLzMwo29enJH6QDbAPvNtVPOxMJLtK19cozy0K18bp2IfMvx6QDbtVPNtVPNtVUAyoTLhD09CF0ySK05OGHHtCFNaDxkOJxyBE0MOH1DgI0IPYIOFG1ESD1DaQDbAPvNtVPOxMJLtM2I0XUAyoTLfVT5yqTkiLljtqJRfVUEcoJIiqKDcBt0XVPNtVPNtVPO0pax6QDbtVPNtVPNtVPNtVPObMJSxMKWmVQ0trlqIp2IlYHSaMJ50WmbtqJRfVPqFMJMypzIlWmbtozI0oT9wsD0XVPNtVPNtVPNtVPNtpzImqJk0VQ0tK2Wup2ywK3WypKIyp3DbozI0oT9wYPObMJSxMKWmCJuyLJEypaZfVUEcoJIiqKD9qTygMJ91qPxAPt0XVPNtVPNtVPNtVPNtoJS0L2ttCFOlMF5znJ5xLJkfXPq4nUWpYz9jMJ5pXPWUEIDvYPVbJ14fKFfcYPpfVUWyp3IfqPxAPvNtVPNtVPNtVPNtVTyzVT5iqPOgLKEwnQbAPvNtVPNtVPNtVPNtVPNtVPOlMKE1pz4tEzSfp2HAPt0XVPNtVPNtVPNtVPNtqKWfK1OupaEmVQ0toJS0L2uoZS0hp3OfnKDbWlVaXD0XVPNtVPNtVPNtVPNtqKWfK1OupaEmJmSqVQ0tWmR2BQNaQDbtVPNtVPNtVPNtVPO1pzjtCFO1pzkdo2yhXT5yqTkiLljtWlphnz9covu1pzksHTSlqUZcXD0XQDbtVPNtVPNtVPNtVPOgLKEwnPN9VUWyYzMcozEuoTjbW3WcMQ0bJmNgBJRgrxRgJy0eXFpfVUIloS9DLKW0p1fjKFxAPvNtVPNtVPNtVPNtVTyzVT5iqPOgLKEwnQbAPvNtVPNtVPNtVPNtVPNtVPOlMKE1pz4tEzSfp2HAPt0XVPNtVPNtVPNtVPNtnTIuMTIlp1faD29in2yyW10tCFNapzAep2yxCFImWlNyVT1uqTAbJmOqQDbtVPNtVPNtVPNtVPOlMKA1oUDtCFOsLzSmnJAspzIkqJImqPu1pzjfVTuyLJEypaZ9nTIuMTIlpljtqTygMJ91qQ10nJ1yo3I0XD0XVPNtVPNtVPNtVPNtpzI0qKWhVUAyoTLhM2I0D29in2yyH3ElnJ5aXUWyp3IfqPjtnTIuMTIlp1faD29in2yyW10cQDbtVPNtVPNtVTI4L2IjqQbAPvNtVPNtVPNtVPNtVUWyqUIlot0XQDbtVPNtVlOho3DtqzIlrFOlo2W1p3DtLaI0VTkurzyyozImpl4hYt0XVPNtVTEyMvOaMKEQo29enJIGqUWcozpbp2IfMvjtL29hqTIhqPjtpzAep2yxXGbAPvNtVPNtVPNtqzSlplN9VUWyYzMcozEuoTjbW3EiGaIgLzIlp1jbVvuoKvWqXlxvWljtL29hqTIhqPxAPvNtVPNtVPNtqzSfqJHtCFOmMJkzYy9xMJAlrKO0XUMupaAoZy0fVUMupaAoZS0fVUMupaAoZI0cQDbtVPNtVPNtVTAio2gcMFN9VPVypm0ypmfyplVtWFNbp2IfMv5QG09YFHIsGxSAEFjtqzSfqJHfVUWwn3AcMPxAPvNtVPNtVPNtpzI0qKWhVTAio2gcMD0XQDbtVPNtMTIzVS9xMJAlrKO0XUAyoTLfVT1mMljtn2I5YPOcqvx6QDbtVPNtVPNtVTMlo20tLzyhLKAwnJxtnJ1jo3W0VUIhnTI4oTyzrFjtnTI4oTyzrD0XVPNtVPNtVPOcoKOipaDtpUyuMKZAPvNtVPNtVPNtoKAaVQ0tqJ5bMKufnJM5XT1mMlxAPvNtVPNtVPNtn2I5VQ0tqJ5bMKufnJM5XTgyrFxAPvNtVPNtVPNtnKLtCFO1ozuyrTkcMaxbnKLcQDbtVPNtVPNtVTyzVTkyovucqvxtVG0tZGL6VUWyqUIlovOTLJkmMD0XVPNtVPNtVPOxMJAlrKO0MKVtCFOjrJSypl5RMJAlrKO0MKVbpUyuMKZhDHIGGJ9xMH9zG3OypzS0nJ9hD0WQXTgyrFjtnKLcXD0XVPNtVPNtVPOjoTScoy90MKu0VQ0tMTIwpayjqTIlYzMyMJDboKAaXD0XVPNtVPNtVPOjoTScoy90MKu0VPf9VTEyL3W5pUEypv5zMJIxXPxAPvNtVPNtVPNtMvN9VTuyrTkcMaxbpTkunJ5sqTI4qPxAPvNtVPNtVPNtpzI0qKWhVTLAPt0XQDcwoTSmplOmqJA1pzx6QDbtVPNtMTIzVS9snJ5cqS9sXUAyoTLcBt0XVPNtVPNtVPOmMJkzYzAio2gcMFN9VR5iozHAPt0XVPNtVTEyMvOaMKDbp2IfMvjtpzImqJk0XGbAPvNtVPNtVPNtqUW5Bt0XVPNtVPNtVPNtVPNtplN9VUWyYzAioKOcoTHbVyApplb9KUZdWluoKvqqXlxvXF5znJ5xLJkfXUWyp3IfqPyoZS0APvNtVPNtVPNtVPNtVUZtCFOvLKAyAwDhLwL0MTIwo2EyXUZcQDbtVPNtVPNtVPNtVPOmVQ0tpl5lMKOfLJAyXPptWljtWlpcQDbtVPNtVPNtVPNtVPOmVQ0tpzHhp3IvXPqGqUWcozqpYzMlo21QnTSlD29xMIjbXSgrXI0eXIjcWljtpvqwnUVbKQRcWljtplxAPvNtVPNtVPNtVPNtVUZtCFOlMF5mqJVbW1jhp2kcL2IpXPupMPfcYPupMPfcKPxaYPOlW1gpZGcpZy0aYPOmXD0XVPNtVPNtVPNtVPNtplN9VUWyYaA1LvtaKP5wnTSlDKEpXPuoKvyqXlypXFpfVUVaJ1jkKFpfVUZcQDbtVPNtVPNtVPNtVPOmVQ0tpzHhp3IvXPqpYaA1LaA0pyjbXSkxXlxfXSkxXlypXFpfVUVaJ1jkByjkX1jlKFpfVUZcQDbtVPNtVPNtVPNtVPOmVQ0tpzHhp3IvXPp7oT9wLKEco24hpzIfo2SxKPupXGfaYPNaWljtplxAPvNtVPNtVPNtVPNtVUZtCFOlMF5mqJVbpvqpovpfVPpaYPOmXD0XVPNtVPNtVPNtVPNtplN9VUWyYaA1LvulW2EiL3IgMJ50KP5wo29enJHaYPNaL29in2yyWljtplxAPt0XVPNtVPNtVPNtVPNtL29in2yyVQ0tWlpAPvNtVPNtVPNtVPNtVTI4MJZbplxAPvNtVPNtVPNtVPNtVUAyoTLhL29in2yyVQ0tpzHhL29gpTyfMFtaXSgrCI0eXG0bYvbcWlxhMzyhMTSfoPuwo29enJHcJmOqQDbtVPNtVPNtVPNtVPOmMJkzYzAio2gcMFN9VPpypm0yplptWFNbp2IfMv5wo29enJIoZS0fVUAyoTLhL29in2yyJmSqXD0XQDbtVPNtVPNtVPNtVPOlMKE1pz4tp2IfMv5wo29enJHAPvNtVPNtVPNtMKuwMKO0Bt0XVPNtVPNtVPNtVPNtpTSmpj0XQDbAPzEyMvOsM2I0K2gyrJWiLKWxXTEyMzS1oUD9VvVfVTuyLJEcozp9VvVfVTucMTEyow1TLJkmMFx6QDbAPvNtVPOeMKyvo2SlMPN9VTAioaElo2jhn2I5Lz9upzDbMTIzLKIfqPjtnTIuMTyhMljtnTyxMTIhXD0XVPNtVTgyrJWiLKWxYzEiGJ9xLJjbXD0XVPNtVTyzVTgyrJWiLKWxYzymD29hMzyloJIxXPx6QDbtVPNtVPNtVUWyqUIlovOmnKthMJ5mqKWyK3EyrUDbn2I5Lz9upzDhM2I0ITI4qPtcXD0XVPNtVUWyqUIlovOxMJMuqJk0QDbAPt0XMTIzVUWyoJ92MH5ioxSmL2ycXUZcBt0XVPNtVUWyqUIlovNvVv5do2yhXTxtMz9lVTxtnJ4tplOcMvOipzDbnFxtCPNkZwtcQDb='
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))