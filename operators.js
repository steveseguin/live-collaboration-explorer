function createMultiOperatorScenario() {
  return {
    id: 'operators', name: 'Multi-operator console', sub: 'Listings, chat & moderation', icon: 'screen',
    category: 'Shared event operations', title: 'One show. A team at the controls.',
    description: 'Several operators manage listings, chat, and moderation from shared controls or a compact popout. No camera or guest call is needed.',
    facts: ['Multiple signed-in operators', 'Scoped event controls', 'No video contribution'],
    audience: 'One existing show', commerce: 'Seller keeps order ownership', basis: 'Control-only concept',
    buyerTitle: 'The same show. More hands behind it.',
    buyerText: 'Operators pin items, answer chat, and moderate behind the scenes. They do not appear in the broadcast or become sellers of record.',
    caption: 'An operator entry opens event controls on another screen or device. The broadcaster keeps publishing as usual.',
    roomCaption: 'A standalone operator popout combines the listing queue, chat, moderation, and permitted event actions. No media room is required.',
    question: 'Does every operator need a full console, or should each role get a focused set of controls?',
    options: [
      option('Shared host console', 'Signed-in teammates work in the same event console.', ['Full console', 'Backend permissions'], 'Reuse the workspace', [node('Signed-in team', 'Individual scoped access', 'people'), node('Event backend', 'Authorize + serialize actions', 'sliders'), node('Shared console state', 'Updates reach every operator', 'screen')], 'An operator invitation in the host console; each teammate opens their own authorized session.', 'Concurrent changes need fresh state, conflict handling, per-action permissions, and an activity trail.'),
      option('Operator popout', 'Detach listings, chat, moderation, and selected event actions.', ['Compact window', 'No media SDK'], 'Focused first prototype', [node('Operator popout', 'Listings + chat + moderation', 'screen'), node('Event API', 'Permission-checked commands', 'sliders'), node('Live updates', 'State + actor acknowledgements', 'broadcast')], 'An Open operator controls action beside the console tools; the popout can run on another device.', 'Detaching the UI is only part of the work. Reconnects, stale actions, and role enforcement still matter.'),
      option('Role-specific desks', 'Give listing runners, moderators, and event leads separate views.', ['Role-based UI', 'Task ownership'], 'For a larger team', [node('Role workspaces', 'Listings / moderation / event', 'people'), node('Event authority', 'Validate role + current state', 'sliders'), node('All clients', 'Consistent event + action log', 'screen')], 'Standalone operator pages, with a lightweight team/status panel in the main console.', 'More UI surfaces and role design; decide which actions require an owner and how operator handoffs work.')
    ]
  };
}

function operatorWindowBar(label) {
  return `<div class="windowbar"><span class="window-dots"><i></i><i></i><i></i></span><span>${label}</span><span>↗</span></div>`;
}

function operatorQueue() {
  return ['Vintage card set', 'Collector edition', 'Sealed pack'].map((title, index) => `<div class="op-queue-item">${product()}<div><strong>${title}</strong><small>${index === 0 ? 'Pinned by Sam · $45' : 'In the event queue'}</small></div><span class="op-chip ${index === 0 ? 'op-selected' : ''}">${index === 0 ? 'On stage' : 'Pin next'}</span></div>`).join('');
}

function operatorMessages() {
  return `<div class="op-chat-message"><strong>cardfan</strong><p>Can you show the back of the card?</p><span>Reply · Pin message</span></div><div class="op-chat-message op-team-message"><strong>Sam · event team</strong><p>Yes! Alex is turning it over now.</p><span>Sent by Sam</span></div><div class="op-chat-message"><strong>miles88</strong><p>Is combined shipping available?</p><span>Reply · Pin message</span></div><div class="op-compose">Reply as event team… <span>Send</span></div>`;
}

function renderMultiOperator(view) {
  if (view === 'buyer') {
    return `<div class="viewer-layout"><div><div class="phone">${phoneTop()}<div class="phone-inner"><div class="phone-heading">ebay Live <span>● LIVE</span></div><div class="phone-videos">${person('host', 'Alex', 'Host')}</div><div class="phone-product"><div><strong>Collector edition · $45</strong><small>Sold by Alex’s Collectibles</small></div><span class="phone-bid">Bid $50</span></div><div class="phone-chat">Sam · event team: We’ll show the back next.<br>cardfan: Thanks for the quick answer!</div></div></div><div class="phone-tag">ONE SELLER · ONE BROADCAST</div></div><div class="viewer-legend"><span class="mini-kicker">WHAT VIEWERS SEE</span><h3>The same show. More hands behind it.</h3><p>Operators handle items and chat. Their controls add no video or guest tiles.</p><div class="viewer-pills"><span>Seller owns orders</span><span>Team replies in chat</span></div></div></div>`;
  }
  if (view === 'room') {
    return `<div class="operator-preview"><div class="screen operator-popout">${operatorWindowBar('Operator controls · separate window')}<div class="op-header"><div><span class="op-kicker">SATURDAY COLLECTIBLES</span><h3>Operator controls <span>↗</span></h3></div><span class="op-connected">● Synced to event</span></div><div class="op-presence"><span class="op-avatar">S</span><strong>Sam · listings</strong><span class="op-avatar op-avatar-blue">R</span><strong>Riley · moderation</strong><span class="op-you">Signed in as Sam</span></div><div class="operator-grid"><section class="operator-column"><h4>${ic('bag')} Listings <span>3 queued</span></h4>${operatorQueue()}<div class="op-secondary">Reorder queue · Edit permitted fields</div></section><section class="operator-column"><h4>${ic('people')} Live chat</h4>${operatorMessages()}</section><section class="operator-column"><h4>${ic('sliders')} Moderation & event</h4><div class="op-action-group"><strong>Chat moderation</strong><span>Delete message</span><span>Mute / unmute user</span><span>Review flagged messages</span></div><div class="op-action-group"><strong>Event actions</strong><span>Pin / unpin listing</span><span class="op-owner-only">Start / end auction · event lead</span><span class="op-owner-only">End event · owner only</span></div></section></div><div class="op-activity"><span>Latest action</span> Sam pinned Vintage card set <strong>Applied · visible to team</strong></div></div><div class="operator-caption">Illustrative controls · commands require individual authorization · broadcasting runs separately</div></div>`;
  }
  return `<div class="desktop-layout"><div class="screen operator-launcher">${operatorWindowBar('Host console / stream manager')}<div class="op-header"><div><span class="op-kicker">SATURDAY COLLECTIBLES</span><h3>Run the show, together.</h3></div><span class="mini-live">LIVE</span></div><div class="operator-launch-grid"><div class="operator-column"><h4>Listing queue</h4>${operatorQueue()}</div><div class="operator-launch-main"><div class="op-team-illustration" role="img" aria-label="Three signed-in operators sharing event controls, with no cameras"><span class="op-large-avatar">A<small>Owner</small></span><span class="op-team-line"></span><span class="op-large-avatar op-sam">S<small>Listings</small></span><span class="op-team-line"></span><span class="op-large-avatar op-riley">R<small>Moderation</small></span></div><div class="op-media-note">${ic('screen')} Event controls only · no camera or call</div><button class="mock-cta highlight op-open" data-operator-preview="room">Open operator popout ↗</button><div class="op-role-chips"><span>Listings</span><span>Chat</span><span>Moderation</span><span>Event actions</span></div></div></div><div class="op-activity"><span>Team activity</span> Riley reviewed a flagged message <strong>All operators synced</strong></div></div><div class="callout"><span class="callout-num">1</span><div><strong>Open shared controls</strong><p>Pop out the work panel. Give each teammate the actions their role needs.</p><span class="location">Host console → operator workspace</span></div></div></div>`;
}
