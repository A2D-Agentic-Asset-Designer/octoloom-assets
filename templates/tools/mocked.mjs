// Fully mocked templates (octoloom#285): the agents, the MCP servers AND the LLM are A2D mocks, so the
// network runs without an OpenAI key. The LLM mock answers with scripted scenarios: a tool call per step
// and a final answer per README prompt, a short hint for any other prompt.
//
// v1 (Agent Network 1.0): the Mule broker prefixes every tool with a random id per deployment
// (`<rand10>_get_member`, `<rand10>_Holds_Agent`), so each step is matched on the tool position N
// (`body.tools.N.name` ends with `_<name>`) and the call reuses that name (`{{body.tools.N.name}}`).
// v2 (Agent Network 2.0): tools are `<action>-client__<tool>` (MCP) and `<action>-client` (A2A).
// A generator/subagent with outputs gets a JSON text answer with `result` as an object; nodes without
// outputs get a structured answer with a string result.

const sk = (id, name, description, examples, tags = []) => ({ id, name, description, examples, tags });
const tool = (name, description, input, cases, fallback, required) => ({ name, description, input, cases, fallback, required: required ?? Object.keys(input).slice(0, 1) });
const MSG = '{!@request.payload.message.parts[0].text}';
const echo = (id, text) => `echo ${id}:
  kind: "a2a:status_update_event"
  state: "TASK_STATE_COMPLETED"
  message: a2a.message({messageId: uuid(), parts: [a2a.textPart(${text})]})
`;
const enumProp = (name, desc, values, ind = '      ') => `${ind}${name}:
${ind}  type: "string"
${ind}  description: "${desc}"
${ind}  enum:
${values.map((v) => `${ind}    - "${v}"`).join('\n')}`;
const strProp = (name, desc, ind = '      ') => `${ind}${name}:
${ind}  type: "string"
${ind}  description: "${desc}"`;

const MOCK_NOTE = 'Fully mocked: the LLM is an A²D LLM mock too, so no OpenAI key is needed.';

// ─────────────────────────────── use cases ───────────────────────────────
export const MOCKED_USECASES = [
  {
    id: 'v1-hotel-concierge', version: 'v1', mocked: true,
    title: 'Hotel Concierge (fully mocked)',
    summary: `A concierge broker books the spa and room service for hotel guests after a reservation lookup. ${MOCK_NOTE}`,
    broker: { key: 'concierge-broker', name: 'Concierge Broker', instructions: [
      'You are the concierge of a hotel.',
      'Always look up the reservation for the room number in the request first (for example room 412).',
      'Use the Spa Booking agent for spa and wellness requests and the Room Service agent for food and drinks in the room.',
      'Answer with the booking or order reference and the time.',
    ], skills: [sk('guest-request', 'Guest Request', 'Handle spa, room service and stay questions for a hotel guest.', ['Book a spa massage for room 412 tomorrow at 10:00', 'Room 415 wants breakfast in the room at 07:30'], ['hospitality'])] },
    agents: [
      { key: 'spa-booking-agent', name: 'Spa Booking Agent', platform: 'AgentForce', proto: '0.3.0', description: 'Books spa and wellness treatments for hotel guests.',
        skills: [sk('book-spa', 'Book Spa', 'Book a spa treatment for a guest.', ['Book a massage for room 412'], ['spa'])],
        replies: [['412', 'Spa booking SPA-7731: 60-minute massage for Mara Keller tomorrow at 10:00; Platinum guests get 20% off.']], fallback: 'Spa booking confirmed.' },
      { key: 'room-service-agent', name: 'Room Service Agent', platform: 'MuleSoft', proto: '0.3.0', description: 'Takes food and drink orders delivered to the room.',
        skills: [sk('order-room-service', 'Order Room Service', 'Order food or drinks to a room.', ['Breakfast for room 415 at 07:30'], ['room-service'])],
        replies: [['415', 'Room service order RS-2208: continental breakfast for 2 to room 415 at 07:30.']], fallback: 'Room service order placed.' },
    ],
    mcps: [
      { key: 'reservations-mcp', name: 'Reservations MCP', description: 'Hotel reservations by room.', tools: [
        tool('get_reservation', 'Get the reservation of a room.', { room: ['string', 'Room number, e.g. 412'] },
          [['room', '412', { room: '412', guest: 'Mara Keller', checkout: '2026-11-24', tier: 'Platinum' }], ['room', '415', { room: '415', guest: 'Tom Berg', checkout: '2026-11-22', tier: 'Standard' }]],
          { error: 'no reservation for this room' }),
      ] },
    ],
    llm: {
      hint: 'This fully mocked concierge answers the README prompts: a spa massage for room 412, breakfast for room 415, the checkout of room 412.',
      plans: [
        { when: ['412', 'spa'], steps: [{ tool: 'get_reservation', args: { room: '412' } }, { agent: 'Spa_Booking_Agent', input: 'Book a 60-minute massage for room 412 tomorrow at 10:00' }], answer: 'Mara Keller (room 412, Platinum) is booked. {{last_tool_output.artifacts.0.parts.0.text}}' },
        { when: ['415', 'breakfast'], steps: [{ tool: 'get_reservation', args: { room: '415' } }, { agent: 'Room_Service_Agent', input: 'Continental breakfast for 2 to room 415 at 07:30' }], answer: 'Tom Berg (room 415) gets breakfast. {{last_tool_output.artifacts.0.parts.0.text}}' },
        { when: ['412', 'checkout'], steps: [{ tool: 'get_reservation', args: { room: '412' } }], answer: 'Mara Keller in room 412 (Platinum) checks out on 2026-11-24.' },
      ],
    },
  },
  {
    id: 'v1-library-services', version: 'v1', mocked: true,
    title: 'Library Services (fully mocked)',
    summary: `A library broker answers member, loan, catalog and event questions with two agents and three tool servers. ${MOCK_NOTE}`,
    broker: { key: 'library-broker', name: 'Library Broker', instructions: [
      'You help members of a public library.',
      'Look up the member (for example M-310) before you answer questions about their loans.',
      'Search the catalog before you ask the Holds agent to place a hold, and use the Events agent for workshops and events.',
      'Answer with titles, due dates and references.',
    ], skills: [sk('library-help', 'Library Help', 'Loans, holds and events for library members.', ['Which loans does member M-310 have?', 'Place a hold on Dune for member M-310'], ['library'])] },
    agents: [
      { key: 'holds-agent', name: 'Holds Agent', platform: 'Azure', proto: '0.3.0', description: 'Places and manages holds on books that are on loan.',
        skills: [sk('place-hold', 'Place Hold', 'Place a hold on a title for a member.', ['Place a hold on Dune for M-310'], ['holds'])],
        replies: [['Dune', 'Hold H-9120 placed on Dune for M-310: position 1, pick up at the Central branch.']], fallback: 'Hold placed.' },
      { key: 'events-agent', name: 'Events Agent', platform: 'AgentForce', proto: '0.3.0', description: 'Knows the library workshops and events.',
        skills: [sk('list-events', 'List Events', 'List upcoming workshops and events.', ['Which workshops are on next week?'], ['events'])],
        replies: [['workshop', 'Next week: Intro to 3D printing (Tuesday 18:00) and Family coding club (Saturday 10:00), both free with a library card.']], fallback: 'No events next week.' },
    ],
    mcps: [
      { key: 'members-mcp', name: 'Members MCP', description: 'Library members.', tools: [
        tool('get_member', 'Get a library member.', { member_id: ['string', 'Member id, e.g. M-310'] }, [['member_id', 'M-310', { member_id: 'M-310', name: 'Ines Moreau', status: 'active', max_loans: 5 }]], { error: 'member not found' }),
      ] },
      { key: 'loans-mcp', name: 'Loans MCP', description: 'Current loans per member.', tools: [
        tool('get_loans', 'List the current loans of a member.', { member_id: ['string', 'Member id'] }, [['member_id', 'M-310', { member_id: 'M-310', loans: [{ title: 'The Left Hand of Darkness', due: '2026-11-27' }, { title: 'Piranesi', due: '2026-12-02' }] }]], { loans: [] }),
      ] },
      { key: 'catalog-mcp', name: 'Library Catalog MCP', description: 'The library catalog.', tools: [
        tool('search_books', 'Search the catalog by title.', { title: ['string', 'Title or part of it'] }, [['title', 'Dune', { title: 'Dune', copies: 3, available: 0, next_return: '2026-11-25' }]], { results: [] }),
      ] },
    ],
    llm: {
      hint: 'This fully mocked library answers the README prompts: the loans of member M-310, a hold on Dune, the workshops next week.',
      plans: [
        { when: ['M-310', 'loans'], steps: [{ tool: 'get_member', args: { member_id: 'M-310' } }, { tool: 'get_loans', args: { member_id: 'M-310' } }], answer: 'Ines Moreau (M-310) has 2 loans: The Left Hand of Darkness (due 2026-11-27) and Piranesi (due 2026-12-02).' },
        { when: ['Dune', 'hold'], steps: [{ tool: 'search_books', args: { title: 'Dune' } }, { agent: 'Holds_Agent', input: 'Place a hold on Dune for member M-310' }], answer: 'All 3 copies of Dune are on loan (next return 2026-11-25). {{last_tool_output.artifacts.0.parts.0.text}}' },
        { when: ['workshop'], steps: [{ agent: 'Events_Agent', input: 'Which workshops are on next week?' }], answer: '{{last_tool_output.artifacts.0.parts.0.text}}' },
      ],
    },
  },
  {
    id: 'v1-fleet-maintenance', version: 'v1', mocked: true,
    title: 'Fleet Maintenance (fully mocked)',
    summary: `A fleet broker checks telematics, orders parts, books the workshop and finds a replacement truck: two agents, four tool servers. ${MOCK_NOTE}`,
    broker: { key: 'fleet-broker', name: 'Fleet Broker', instructions: [
      'You keep a delivery fleet on the road.',
      'For a repair, read the vehicle status first (for example TRK-77), check the part, book a workshop slot and ask the Dispatch agent for a replacement vehicle.',
      'Use the Warranty agent for warranty questions and the fuel tools for fuel budgets.',
      'Answer with the references and dates.',
    ], skills: [sk('fleet-request', 'Fleet Request', 'Repairs, warranty and fuel budgets for fleet vehicles.', ['TRK-77 reports brake wear, get it fixed', 'Is TRK-77 still under warranty?'], ['fleet'])] },
    agents: [
      { key: 'dispatch-agent', name: 'Dispatch Agent', platform: 'MuleSoft', proto: '0.3.0', description: 'Plans routes and replacement vehicles.',
        skills: [sk('replace-vehicle', 'Replace Vehicle', 'Find a replacement vehicle for a route.', ['Find a replacement for TRK-77'], ['dispatch'])],
        replies: [['TRK-77', 'TRK-80 replaces TRK-77 on route R-14 on 2026-11-23.']], fallback: 'A replacement vehicle is planned.' },
      { key: 'warranty-agent', name: 'Warranty Agent', platform: 'Snowflake', proto: '0.3.0', description: 'Knows the warranty terms of every vehicle.',
        skills: [sk('check-warranty', 'Check Warranty', 'Check the warranty of a vehicle.', ['Is TRK-77 under warranty?'], ['warranty'])],
        replies: [['TRK-77', 'TRK-77 drivetrain warranty is valid until 2027-02-28; brake pads are wear parts and not covered.']], fallback: 'No warranty on record.' },
    ],
    mcps: [
      { key: 'telematics-mcp', name: 'Telematics MCP', description: 'Live vehicle status.', tools: [
        tool('get_vehicle_status', 'Get the status and alerts of a vehicle.', { vehicle_id: ['string', 'Vehicle id, e.g. TRK-77'] }, [['vehicle_id', 'TRK-77', { vehicle_id: 'TRK-77', odometer_km: 184220, alerts: ['brake pad wear 85%'], location: 'Depot Basel' }], ['vehicle_id', 'TRK-12', { vehicle_id: 'TRK-12', odometer_km: 40110, alerts: [], location: 'Route R-3' }]], { error: 'unknown vehicle' }),
      ] },
      { key: 'parts-mcp', name: 'Parts MCP', description: 'Spare parts stock.', tools: [
        tool('check_part', 'Check the stock of a part for a vehicle.', { vehicle_id: ['string', 'Vehicle id'], part: ['string', 'Part name'] }, [['vehicle_id', 'TRK-77', { part: 'brake pads', sku: 'BP-4410', in_stock: 6 }]], { in_stock: 0 }, ['vehicle_id', 'part']),
      ] },
      { key: 'workshop-mcp', name: 'Workshop MCP', description: 'Workshop slots.', tools: [
        tool('book_slot', 'Book a workshop slot for a vehicle.', { vehicle_id: ['string', 'Vehicle id'], date: ['string', 'Date, YYYY-MM-DD'] }, [['vehicle_id', 'TRK-77', { booking_id: 'WS-5521', date: '2026-11-23', bay: 2 }]], { booking_id: 'WS-0000' }, ['vehicle_id', 'date']),
      ] },
      { key: 'fuel-mcp', name: 'Fuel MCP', description: 'Fuel cards and budgets.', tools: [
        tool('get_fuel_card', 'Get the fuel card and budget of a vehicle.', { vehicle_id: ['string', 'Vehicle id'] }, [['vehicle_id', 'TRK-12', { card: 'FC-1212', limit_chf: 800, used_chf: 615 }]], { error: 'no fuel card' }),
      ] },
    ],
    llm: {
      hint: 'This fully mocked fleet answers the README prompts: the brake repair of TRK-77, the warranty of TRK-77, the fuel budget of TRK-12.',
      plans: [
        { when: ['TRK-77', 'brake'], steps: [
          { tool: 'get_vehicle_status', args: { vehicle_id: 'TRK-77' } },
          { tool: 'check_part', args: { vehicle_id: 'TRK-77', part: 'brake pads' } },
          { tool: 'book_slot', args: { vehicle_id: 'TRK-77', date: '2026-11-23' } },
          { agent: 'Dispatch_Agent', input: 'Find a replacement vehicle for TRK-77 on 2026-11-23' },
        ], answer: 'TRK-77 needs new brake pads (wear 85%). Part BP-4410 is in stock and workshop slot WS-5521 is booked for 2026-11-23 (bay 2). {{last_tool_output.artifacts.0.parts.0.text}}' },
        { when: ['TRK-77', 'warranty'], steps: [{ agent: 'Warranty_Agent', input: 'Is TRK-77 still under warranty?' }], answer: '{{last_tool_output.artifacts.0.parts.0.text}}' },
        { when: ['TRK-12', 'fuel'], steps: [{ tool: 'get_fuel_card', args: { vehicle_id: 'TRK-12' } }], answer: 'Fuel card FC-1212 of TRK-12 has used 615 of 800 CHF this month: 185 CHF left.' },
      ],
    },
  },
  {
    id: 'v2-event-ticketing', version: 'v2', mocked: true,
    title: 'Event Ticketing (fully mocked)',
    summary: `Extract the event, check availability, reserve the seats and issue the tickets, or join the waitlist. ${MOCK_NOTE}`,
    broker: { key: 'ticketing_broker', name: 'Ticketing Broker', skills: [sk('buy-tickets', 'Buy Tickets', 'Buy tickets for an event or join its waitlist.', ['Two tickets for event EV-501 please', 'Four seats for EV-502'], ['events', 'ticketing'])] },
    agents: [
      { key: 'ticketing_agent', name: 'Ticketing Agent', platform: 'MuleSoft', proto: '0.3.0', description: 'Issues e-tickets for reserved seats.', skills: [sk('issue-tickets', 'Issue Tickets', 'Issue the e-tickets of a reservation.', ['Issue the tickets for EV-501'], ['tickets'])],
        replies: [['EV-501', 'E-tickets TK-501-A1 and TK-501-A2 sent by email; doors open at 19:00, Hall 3.']], fallback: 'E-tickets sent.' },
      { key: 'waitlist_agent', name: 'Waitlist Agent', platform: 'AgentForce', proto: '1.0', description: 'Puts customers on the waitlist of sold-out events.', skills: [sk('join-waitlist', 'Join Waitlist', 'Add a customer to a waitlist.', ['Waitlist for EV-502'], ['waitlist'])],
        replies: [['EV-502', 'Waitlist WL-502-19: position 3 for 4 seats; we send an email when seats free up.']], fallback: 'Added to the waitlist.' },
    ],
    mcps: [
      { key: 'events_mcp', name: 'Events MCP', description: 'Event calendar and availability.', tools: [
        tool('check_availability', 'Check the free seats of an event.', { event_id: ['string', 'Event id, e.g. EV-501'] },
          [['event_id', 'EV-501', { event_id: 'EV-501', available: true, seats_left: 38, name: 'Jazz Night' }], ['event_id', 'EV-502', { event_id: 'EV-502', available: false, reason: 'sold out' }]], { available: false, reason: 'event not found' }),
      ] },
      { key: 'booking_mcp', name: 'Booking MCP', description: 'Seat reservations.', tools: [
        tool('reserve_seats', 'Reserve seats for an event.', { event_id: ['string', 'Event id'], seats: ['string', 'Number of seats'] }, [['event_id', 'EV-501', { reservation_id: 'RS-501-7', seats: 2, row: 'F' }]], { reservation_id: 'RS-000' }, ['event_id', 'seats']),
      ] },
    ],
    llm: {
      hint: 'This fully mocked ticket desk answers the README prompts: two tickets for EV-501 (available) and four seats for EV-502 (sold out).',
      gen: { field: 'event_id', cases: [['EV-501', { event_id: 'EV-501', seats: '2' }], ['EV-502', { event_id: 'EV-502', seats: '4' }]], fallback: { event_id: 'UNKNOWN', seats: '0' } },
      gate: { field: 'available', action: 'check_availability', cases: [['EV-501', { event_id: 'EV-501' }], ['EV-502', { event_id: 'EV-502' }]], yesPath: 'content.available', yes: { available: 'yes', detail: '{{last_tool_output.content.seats_left}} seats left' }, no: { available: 'no', detail: '{{last_tool_output.content.reason}}' }, fallback: { available: 'no', detail: 'unknown event' } },
      agents: [
        { action: 'ticketing_agent', cases: [['EV-501', 'Issue the e-tickets for event EV-501, 2 seats']] },
        { action: 'waitlist_agent', cases: [['EV-502', 'Add the customer to the waitlist of event EV-502 for 4 seats']] },
      ],
    },
  },
  {
    id: 'v2-warranty-repair', version: 'v2', mocked: true,
    title: 'Warranty Repair (fully mocked)',
    summary: `Check the device warranty: covered repairs are booked and confirmed, the others get a quote. Three agents, one tool server. ${MOCK_NOTE}`,
    broker: { key: 'repair_broker', name: 'Repair Broker', skills: [sk('repair-device', 'Repair a Device', 'Repair a device under warranty or get a quote.', ['My laptop SN-1001 has a flickering screen', 'SN-2002 has a swollen battery'], ['repair', 'warranty'])] },
    agents: [
      { key: 'repair_agent', name: 'Repair Agent', platform: 'MuleSoft', proto: '0.3.0', description: 'Books warranty repairs with courier pickup.', skills: [sk('book-repair', 'Book Repair', 'Book a warranty repair.', ['Book a repair for SN-1001'], ['repair'])],
        replies: [['SN-1001', 'Repair RP-1001 booked: courier pickup tomorrow 09:00-12:00, screen replacement free of charge.']], fallback: 'Repair booked.' },
      { key: 'notify_agent', name: 'Notification Agent', platform: 'Vertex', proto: '1.0', description: 'Sends confirmations by SMS and email.', skills: [sk('notify-owner', 'Notify Owner', 'Confirm a repair to the owner.', ['Confirm RP-1001'], ['notify'])],
        replies: [['SN-1001', 'Confirmation for RP-1001 sent by SMS and email.']], fallback: 'Confirmation sent.' },
      { key: 'quote_agent', name: 'Quote Agent', platform: 'AgentForce', proto: '1.0', description: 'Quotes repairs outside warranty.', skills: [sk('quote-repair', 'Quote Repair', 'Quote a paid repair.', ['Quote a battery for SN-2002'], ['quote'])],
        replies: [['SN-2002', 'Quote QT-2002: battery replacement 89.00 CHF, ready in 3 working days.']], fallback: 'Quote sent.' },
    ],
    mcps: [
      { key: 'device_registry_mcp', name: 'Device Registry MCP', description: 'Registered devices and their warranty.', tools: [
        tool('check_warranty', 'Check the warranty of a device by serial number.', { serial: ['string', 'Serial number, e.g. SN-1001'] },
          [['serial', 'SN-1001', { serial: 'SN-1001', covered: true, until: '2027-05-31', model: 'Notebook 14' }], ['serial', 'SN-2002', { serial: 'SN-2002', covered: false, reason: 'warranty expired on 2026-03-01' }]], { covered: false, reason: 'device not registered' }),
      ] },
    ],
    llm: {
      hint: 'This fully mocked repair desk answers the README prompts: SN-1001 (under warranty) and SN-2002 (expired).',
      gen: { field: 'serial', cases: [['SN-1001', { serial: 'SN-1001', issue: 'flickering screen' }], ['SN-2002', { serial: 'SN-2002', issue: 'swollen battery' }]], fallback: { serial: 'UNKNOWN', issue: 'unknown' } },
      gate: { field: 'covered', action: 'check_warranty', cases: [['SN-1001', { serial: 'SN-1001' }], ['SN-2002', { serial: 'SN-2002' }]], yesPath: 'content.covered', yes: { covered: 'yes', detail: 'covered until {{last_tool_output.content.until}}' }, no: { covered: 'no', detail: '{{last_tool_output.content.reason}}' }, fallback: { covered: 'no', detail: 'device not registered' } },
      agents: [
        { action: 'repair_agent', cases: [['SN-1001', 'Book a warranty repair for SN-1001: flickering screen']] },
        { action: 'notify_agent', cases: [['SN-1001', 'Confirm the repair of SN-1001 to the owner']] },
        { action: 'quote_agent', cases: [['SN-2002', 'Quote a paid repair for SN-2002: swollen battery']] },
      ],
    },
  },
  {
    id: 'v2-utility-outage', version: 'v2', mocked: true,
    title: 'Utility Outage (fully mocked)',
    summary: `A known outage gets status updates and a bill credit; an unknown one gets a ticket and a field crew. Three agents, two tool servers. ${MOCK_NOTE}`,
    broker: { key: 'outage_broker', name: 'Outage Broker', skills: [sk('report-outage', 'Report an Outage', 'Report a power outage at an address.', ['No power at ADDR-31 since this morning', 'The lights flicker at ADDR-44'], ['utilities', 'outage'])] },
    agents: [
      { key: 'comms_agent', name: 'Customer Comms Agent', platform: 'AgentForce', proto: '1.0', description: 'Sends outage status updates to customers.', skills: [sk('outage-updates', 'Outage Updates', 'Subscribe a customer to outage updates.', ['Updates for ADDR-31'], ['comms'])],
        replies: [['ADDR-31', 'SMS updates for outage OUT-778 enabled for ADDR-31: power is back by 18:30.']], fallback: 'Updates enabled.' },
      { key: 'credit_agent', name: 'Billing Credit Agent', platform: 'MuleSoft', proto: '0.3.0', description: 'Applies bill credits for outages.', skills: [sk('outage-credit', 'Outage Credit', 'Apply a bill credit for an outage.', ['Credit ADDR-31'], ['billing'])],
        replies: [['ADDR-31', 'Bill credit CR-31 of 15.00 CHF applied for the outage.']], fallback: 'Credit applied.' },
      { key: 'crew_agent', name: 'Crew Dispatch Agent', platform: 'Azure', proto: '1.0', description: 'Dispatches field crews.', skills: [sk('dispatch-crew', 'Dispatch Crew', 'Send a crew to an address.', ['Send a crew to ADDR-44'], ['field'])],
        replies: [['ADDR-44', 'Crew C-12 dispatched to ADDR-44, arrival in about 45 minutes.']], fallback: 'Crew dispatched.' },
    ],
    mcps: [
      { key: 'grid_mcp', name: 'Grid MCP', description: 'Known outages on the grid.', tools: [
        tool('get_outage', 'Get the known outage at an address.', { address_id: ['string', 'Address id, e.g. ADDR-31'] },
          [['address_id', 'ADDR-31', { address_id: 'ADDR-31', known: true, outage_id: 'OUT-778', restore_eta: '18:30' }], ['address_id', 'ADDR-44', { address_id: 'ADDR-44', known: false, reason: 'no known outage at this address' }]], { known: false, reason: 'address not found' }),
      ] },
      { key: 'field_ticket_mcp', name: 'Field Ticket MCP', description: 'Field service tickets.', tools: [
        tool('create_ticket', 'Create a field ticket for an address.', { address_id: ['string', 'Address id'], symptom: ['string', 'What the customer sees'] }, [['address_id', 'ADDR-44', { ticket_id: 'FT-4401', priority: 'high' }]], { ticket_id: 'FT-0000' }, ['address_id', 'symptom']),
      ] },
    ],
    llm: {
      hint: 'This fully mocked outage desk answers the README prompts: ADDR-31 (known outage) and ADDR-44 (new ticket and crew).',
      gen: { field: 'address_id', cases: [['ADDR-31', { address_id: 'ADDR-31', symptom: 'no power' }], ['ADDR-44', { address_id: 'ADDR-44', symptom: 'flickering lights' }]], fallback: { address_id: 'UNKNOWN', symptom: 'unknown' } },
      gate: { field: 'known', action: 'get_outage', cases: [['ADDR-31', { address_id: 'ADDR-31' }], ['ADDR-44', { address_id: 'ADDR-44' }]], yesPath: 'content.known', yes: { known: 'yes', detail: 'outage {{last_tool_output.content.outage_id}}, back by {{last_tool_output.content.restore_eta}}' }, no: { known: 'no', detail: '{{last_tool_output.content.reason}}' }, fallback: { known: 'no', detail: 'address not found' } },
      agents: [
        { action: 'comms_agent', cases: [['ADDR-31', 'Enable outage updates for ADDR-31']] },
        { action: 'credit_agent', cases: [['ADDR-31', 'Apply the outage bill credit for ADDR-31']] },
        { action: 'crew_agent', cases: [['ADDR-44', 'Send a field crew to ADDR-44: flickering lights']] },
      ],
    },
  },
];

// ─────────────────────────────── v2 flows ───────────────────────────────
export const MOCKED_FLOWS = {
  'v2-event-ticketing': {
    system: 'You are the box office of a concert hall. Reserve seats only when the event has free seats.',
    actions: { check_availability: { mcp: 'events_mcp', tool: 'check_availability' }, reserve_seats: { mcp: 'booking_mcp', tool: 'reserve_seats', inputs: { event_id: 'string', seats: 'string' } }, ticketing_agent: { a2a: 'ticketing_agent' }, waitlist_agent: { a2a: 'waitlist_agent' } },
    start: '@generator.extractBooking',
    body: `# Step 1: one LLM call turns the request into an event id and a seat count.
generator extractBooking:
  description: "Extracts the event id and the number of seats."
  label: "Extract Booking"
  system:
    instructions: |
      Extract the event id (for example EV-501) and the number of seats from the message.
      Use "UNKNOWN" when no event id is present.
  prompt: ->
    | ${MSG}
  outputs:
    properties:
${strProp('event_id', 'Event id, e.g. EV-501, or UNKNOWN')}
${strProp('seats', 'Number of seats')}
  on_exit: ->
    transition to @subagent.availabilityGate

# Step 2: a gate. The subagent calls the Events MCP and classifies the answer.
subagent availabilityGate:
  description: "Checks the free seats with the Events MCP."
  label: "Availability Gate"
  system:
    instructions: |
      Call the availability tool for the event and report whether seats are free.
      Set available to "yes" only when the tool returns available true.
  reasoning:
    instructions: ->
      | Event: {!@generator.extractBooking.output.event_id}. Request: ${MSG}
    actions:
      check: @actions.check_availability
    max_number_of_loops: 3
    outputs:
      properties:
${enumProp('available', 'Whether seats are free', ['yes', 'no'], '        ')}
${strProp('detail', 'Availability detail from the tool', '        ')}
  on_exit: ->
    transition to @router.availabilityRouter

router availabilityRouter:
  description: "Free seats are reserved and ticketed; sold-out events go to the waitlist."
  routes:
    - target: @executor.reserveSeats
      when: @subagent.availabilityGate.output.available == "yes"
      label: "Available"
  otherwise:
    target: @subagent.joinWaitlist

# Step 3a: no LLM. The seats are reserved with bound arguments only.
executor reserveSeats:
  description: "Reserves the seats."
  do: ->
    run @actions.reserve_seats
      with event_id = @generator.extractBooking.output.event_id
      with seats = @generator.extractBooking.output.seats
  on_exit: ->
    transition to @subagent.issueTickets

subagent issueTickets:
  description: "Issues the e-tickets through the Ticketing agent."
  label: "Issue Tickets"
  reasoning:
    instructions: ->
      | Issue the e-tickets for event {!@generator.extractBooking.output.event_id}, {!@generator.extractBooking.output.seats} seats. Request: ${MSG}
    actions:
      tickets: @actions.ticketing_agent
  on_exit: ->
    transition to @echo.booked

${echo('booked', '"Booked " + @generator.extractBooking.output.seats + " seats for " + @generator.extractBooking.output.event_id + ". " + @subagent.issueTickets.output')}
# Step 3b: sold out. The Waitlist agent takes over.
subagent joinWaitlist:
  description: "Puts the customer on the waitlist."
  label: "Join Waitlist"
  reasoning:
    instructions: ->
      | Event {!@generator.extractBooking.output.event_id} has no free seats: {!@subagent.availabilityGate.output.detail}. Add the customer to the waitlist. Request: ${MSG}
    actions:
      waitlist: @actions.waitlist_agent
  on_exit: ->
    transition to @echo.waitlisted

${echo('waitlisted', '"Sold out: " + @subagent.availabilityGate.output.detail + ". " + @subagent.joinWaitlist.output')}`,
  },
  'v2-warranty-repair': {
    system: 'You are the repair desk of an electronics brand. Repair free of charge only when the registry says the device is covered.',
    actions: { check_warranty: { mcp: 'device_registry_mcp', tool: 'check_warranty' }, repair_agent: { a2a: 'repair_agent' }, notify_agent: { a2a: 'notify_agent' }, quote_agent: { a2a: 'quote_agent' } },
    start: '@generator.extractDevice',
    body: `# Step 1: one LLM call turns the request into a serial number and an issue.
generator extractDevice:
  description: "Extracts the serial number and the issue."
  label: "Extract Device"
  system:
    instructions: |
      Extract the serial number (for example SN-1001) and a short issue from the message.
      Use "UNKNOWN" when no serial number is present.
  prompt: ->
    | ${MSG}
  outputs:
    properties:
${strProp('serial', 'Serial number, e.g. SN-1001, or UNKNOWN')}
${strProp('issue', 'Short description of the issue')}
  on_exit: ->
    transition to @subagent.warrantyGate

# Step 2: a gate. The subagent calls the Device Registry MCP and classifies the answer.
subagent warrantyGate:
  description: "Checks the warranty with the Device Registry MCP."
  label: "Warranty Gate"
  system:
    instructions: |
      Call the warranty tool for the serial number and report whether the device is covered.
      Set covered to "yes" only when the tool returns covered true.
  reasoning:
    instructions: ->
      | Serial: {!@generator.extractDevice.output.serial}. Request: ${MSG}
    actions:
      check: @actions.check_warranty
    max_number_of_loops: 3
    outputs:
      properties:
${enumProp('covered', 'Whether the device is under warranty', ['yes', 'no'], '        ')}
${strProp('detail', 'Warranty detail from the tool', '        ')}
  on_exit: ->
    transition to @router.warrantyRouter

router warrantyRouter:
  description: "Covered devices get a free repair and a confirmation; the others get a quote."
  routes:
    - target: @subagent.bookRepair
      when: @subagent.warrantyGate.output.covered == "yes"
      label: "Covered"
  otherwise:
    target: @subagent.quoteRepair

# Step 3a: book the repair, then confirm it to the owner.
subagent bookRepair:
  description: "Books the warranty repair through the Repair agent."
  label: "Book Repair"
  reasoning:
    instructions: ->
      | Book a warranty repair for {!@generator.extractDevice.output.serial}: {!@generator.extractDevice.output.issue}. Request: ${MSG}
    actions:
      repair: @actions.repair_agent
  on_exit: ->
    transition to @subagent.notifyOwner

subagent notifyOwner:
  description: "Confirms the repair through the Notification agent."
  label: "Notify Owner"
  reasoning:
    instructions: ->
      | Confirm the repair of {!@generator.extractDevice.output.serial} to the owner. Request: ${MSG}
    actions:
      notify: @actions.notify_agent
  on_exit: ->
    transition to @echo.repairBooked

${echo('repairBooked', '"Under warranty (" + @subagent.warrantyGate.output.detail + "). " + @subagent.bookRepair.output + " " + @subagent.notifyOwner.output')}
# Step 3b: not covered. The Quote agent prices the repair.
subagent quoteRepair:
  description: "Quotes a paid repair."
  label: "Quote Repair"
  reasoning:
    instructions: ->
      | {!@generator.extractDevice.output.serial} is not covered: {!@subagent.warrantyGate.output.detail}. Quote a paid repair for: {!@generator.extractDevice.output.issue}. Request: ${MSG}
    actions:
      quote: @actions.quote_agent
  on_exit: ->
    transition to @echo.quoted

${echo('quoted', '"Not covered: " + @subagent.warrantyGate.output.detail + ". " + @subagent.quoteRepair.output')}`,
  },
  'v2-utility-outage': {
    system: 'You are the outage desk of a power utility. Send a crew only when the grid does not already know the outage.',
    actions: { get_outage: { mcp: 'grid_mcp', tool: 'get_outage' }, create_ticket: { mcp: 'field_ticket_mcp', tool: 'create_ticket', inputs: { address_id: 'string', symptom: 'string' } }, comms_agent: { a2a: 'comms_agent' }, credit_agent: { a2a: 'credit_agent' }, crew_agent: { a2a: 'crew_agent' } },
    start: '@generator.extractOutage',
    body: `# Step 1: one LLM call turns the report into an address id and a symptom.
generator extractOutage:
  description: "Extracts the address id and the symptom."
  label: "Extract Outage"
  system:
    instructions: |
      Extract the address id (for example ADDR-31) and a short symptom from the message.
      Use "UNKNOWN" when no address id is present.
  prompt: ->
    | ${MSG}
  outputs:
    properties:
${strProp('address_id', 'Address id, e.g. ADDR-31, or UNKNOWN')}
${strProp('symptom', 'What the customer sees')}
  on_exit: ->
    transition to @subagent.outageGate

# Step 2: a gate. The subagent asks the Grid MCP whether the outage is known.
subagent outageGate:
  description: "Looks up known outages with the Grid MCP."
  label: "Outage Gate"
  system:
    instructions: |
      Call the outage tool for the address and report whether the outage is already known.
      Set known to "yes" only when the tool returns known true.
  reasoning:
    instructions: ->
      | Address: {!@generator.extractOutage.output.address_id}. Report: ${MSG}
    actions:
      check: @actions.get_outage
    max_number_of_loops: 3
    outputs:
      properties:
${enumProp('known', 'Whether the outage is already known', ['yes', 'no'], '        ')}
${strProp('detail', 'Outage detail from the tool', '        ')}
  on_exit: ->
    transition to @router.outageRouter

router outageRouter:
  description: "Known outages get updates and a credit; new ones get a ticket and a crew."
  routes:
    - target: @subagent.informCustomer
      when: @subagent.outageGate.output.known == "yes"
      label: "Known"
  otherwise:
    target: @executor.createTicket

# Step 3a: a known outage. Updates, then a bill credit.
subagent informCustomer:
  description: "Enables status updates through the Customer Comms agent."
  label: "Inform Customer"
  reasoning:
    instructions: ->
      | Enable outage updates for {!@generator.extractOutage.output.address_id}. Report: ${MSG}
    actions:
      updates: @actions.comms_agent
  on_exit: ->
    transition to @subagent.offerCredit

subagent offerCredit:
  description: "Applies the outage bill credit through the Billing Credit agent."
  label: "Offer Credit"
  reasoning:
    instructions: ->
      | Apply the outage bill credit for {!@generator.extractOutage.output.address_id}. Report: ${MSG}
    actions:
      credit: @actions.credit_agent
  on_exit: ->
    transition to @echo.knownOutage

${echo('knownOutage', '"Known " + @subagent.outageGate.output.detail + ". " + @subagent.informCustomer.output + " " + @subagent.offerCredit.output')}
# Step 3b: a new problem. No LLM for the ticket; the crew is dispatched by the Crew Dispatch agent.
executor createTicket:
  description: "Creates the field ticket."
  do: ->
    run @actions.create_ticket
      with address_id = @generator.extractOutage.output.address_id
      with symptom = @generator.extractOutage.output.symptom
  on_exit: ->
    transition to @subagent.dispatchCrew

subagent dispatchCrew:
  description: "Dispatches a field crew."
  label: "Dispatch Crew"
  reasoning:
    instructions: ->
      | Send a field crew to {!@generator.extractOutage.output.address_id}: {!@generator.extractOutage.output.symptom}. Report: ${MSG}
    actions:
      crew: @actions.crew_agent
  on_exit: ->
    transition to @echo.crewDispatched

${echo('crewDispatched', '"New problem at " + @generator.extractOutage.output.address_id + ": a field ticket is open. " + @subagent.dispatchCrew.output')}`,
  },
};

// ─────────────────────────────── Try it ───────────────────────────────
export const MOCKED_TRY = {
  'v1-hotel-concierge': [
    { p: 'Book a spa massage for room 412 tomorrow at 10:00', see: 'Reservations MCP `get_reservation` finds Mara Keller (Platinum), then the Spa Booking Agent books SPA-7731 at 10:00 with 20% off.' },
    { p: 'Room 415 wants breakfast in the room at 07:30', see: '`get_reservation` finds Tom Berg, then the Room Service Agent places order RS-2208 for 07:30.' },
    { p: 'When is the checkout of room 412?', see: '`get_reservation`: Mara Keller checks out on 2026-11-24.' },
  ],
  'v1-library-services': [
    { p: 'Which loans does member M-310 have?', see: 'Members MCP `get_member` (Ines Moreau) and Loans MCP `get_loans`: The Left Hand of Darkness (due 2026-11-27) and Piranesi (due 2026-12-02).' },
    { p: 'Place a hold on Dune for member M-310', see: 'Library Catalog MCP `search_books`: all 3 copies on loan, next return 2026-11-25. The Holds Agent places hold H-9120 (position 1).' },
    { p: 'Which workshops are on next week?', see: 'The Events Agent lists Intro to 3D printing (Tuesday 18:00) and Family coding club (Saturday 10:00).' },
  ],
  'v1-fleet-maintenance': [
    { p: 'TRK-77 reports brake wear, get it fixed', see: 'Four calls in a row: Telematics `get_vehicle_status` (brake pad wear 85%), Parts `check_part` (BP-4410 in stock), Workshop `book_slot` (WS-5521 on 2026-11-23, bay 2) and the Dispatch Agent (TRK-80 replaces TRK-77 on route R-14).' },
    { p: 'Is TRK-77 still under warranty?', see: 'The Warranty Agent: drivetrain until 2027-02-28, brake pads not covered.' },
    { p: 'How much fuel budget is left for TRK-12?', see: 'Fuel MCP `get_fuel_card`: FC-1212 used 615 of 800 CHF, 185 CHF left.' },
  ],
  'v2-event-ticketing': [
    { p: 'Two tickets for event EV-501 please', see: 'Availability Gate: 38 seats left. Reserve Seats runs `reserve_seats` without the LLM, and the Ticketing Agent sends TK-501-A1 and TK-501-A2. Reply starts with "Booked 2 seats for EV-501".' },
    { p: 'Four seats for EV-502', see: 'Availability Gate: sold out. The Waitlist Agent (A2A 1.0) adds you at position 3 (WL-502-19).' },
  ],
  'v2-warranty-repair': [
    { p: 'My laptop SN-1001 has a flickering screen', see: 'Warranty Gate: covered until 2027-05-31. The Repair Agent books RP-1001 with courier pickup, the Notification Agent confirms it by SMS and email.' },
    { p: 'SN-2002 has a swollen battery', see: 'Warranty Gate: expired on 2026-03-01. The Quote Agent sends QT-2002 (89.00 CHF, 3 working days).' },
  ],
  'v2-utility-outage': [
    { p: 'No power at ADDR-31 since this morning', see: 'Outage Gate: known outage OUT-778, back by 18:30. The Customer Comms Agent enables SMS updates and the Billing Credit Agent applies credit CR-31 (15.00 CHF).' },
    { p: 'The lights flicker at ADDR-44', see: 'Outage Gate: no known outage. Create Ticket runs `create_ticket` without the LLM, and the Crew Dispatch Agent sends crew C-12 (about 45 minutes).' },
  ],
};

// ─────────────────────────────── LLM mock scenarios ───────────────────────────────
const S = (result, flags = { goalComplete: true }) => ({ kind: 'structured_answer', answer: { result, reasoning: 'A²D LLM mock scenario', ...flags } });
const J = (result) => ({ kind: 'text', text: JSON.stringify({ result, reasoning: 'A²D LLM mock scenario', additionalInputRequired: false, goalComplete: true, goalFailed: false, authRequired: false }) });
const say = (v) => ({ source: 'last_user_text', operator: 'contains', value: v });
const has = (f) => ({ source: 'body', field: `text.format.schema.properties.result.properties.${f}`, operator: 'exists', value: '' });
const toolAvail = (t) => ({ source: 'tool_available', operator: 'exists', value: t });
const lastIs = (t) => ({ source: 'last_tool_name', operator: '===', value: t });

function v1Scenarios(u) {
  const n = u.mcps.reduce((k, m) => k + m.tools.length, 0) + u.agents.length + 2;
  const out = [];
  let p = 10;
  for (const [pi, plan] of u.llm.plans.entries()) {
    const when = plan.when.map(say);
    const tag = plan.when.join(' ');
    const names = plan.steps.map((s) => '_' + (s.tool ?? s.agent));
    out.push({ name: `${tag}: answer`, priority: p++, conditions: [...when, { source: 'last_tool_name', operator: 'ends_with', value: names.at(-1) }], response: S(plan.answer) });
    for (let i = plan.steps.length - 1; i >= 0; i--) {
      const s = plan.steps[i];
      for (let k = 0; k < n; k++) {
        const conds = [...when, { source: 'body', field: `tools.${k}.name`, operator: 'ends_with', value: names[i] }];
        if (i > 0) conds.push({ source: 'last_tool_name', operator: 'ends_with', value: names[i - 1] });
        const response = s.tool
          ? { kind: 'tool_call', name: `{{body.tools.${k}.name}}`, toolKind: 'function', arguments: s.args }
          : { kind: 'tool_call', name: `{{body.tools.${k}.name}}`, toolKind: 'custom', input: s.input };
        // The first step runs only when no later step matched: a higher number = a lower priority.
        out.push({ name: `${tag}: step ${i + 1} @${k}`, priority: i === 0 ? 500 + pi : p, conditions: conds, response });
      }
      p++;
    }
  }
  out.push({ name: 'any other prompt', priority: 900, conditions: [], response: S(u.llm.hint) });
  return out;
}

function v2Scenarios(u) {
  const f = MOCKED_FLOWS[u.id];
  const { gen, gate, agents, hint } = u.llm;
  const mcpTool = (action) => `${action}-client__${f.actions[action].tool}`;
  const out = [];
  for (const [kw, obj] of gen.cases) out.push({ name: `extract ${kw}`, priority: 10, conditions: [has(gen.field), say(kw)], response: J(obj) });
  out.push({ name: 'extract: other', priority: 11, conditions: [has(gen.field)], response: J(gen.fallback) });
  const T = mcpTool(gate.action);
  out.push({ name: 'gate: yes', priority: 20, conditions: [has(gate.field), lastIs(T), { source: 'last_tool_output', field: gate.yesPath, operator: '===', value: true }], response: J(gate.yes) });
  out.push({ name: 'gate: no', priority: 21, conditions: [has(gate.field), lastIs(T)], response: J(gate.no) });
  for (const [kw, args] of gate.cases) out.push({ name: `gate: call ${kw}`, priority: 30, conditions: [has(gate.field), say(kw)], response: { kind: 'tool_call', name: T, arguments: args } });
  out.push({ name: 'gate: other', priority: 31, conditions: [has(gate.field)], response: J(gate.fallback) });
  let p = 40;
  for (const a of agents) {
    const t = `${a.action}-client`;
    out.push({ name: `${a.action}: answer`, priority: p++, conditions: [toolAvail(t), lastIs(t)], response: S('{{last_tool_output}}') });
    for (const [kw, message] of a.cases) out.push({ name: `${a.action}: call ${kw}`, priority: p++, conditions: [toolAvail(t), say(kw)], response: { kind: 'tool_call', name: t, arguments: { message } } });
    out.push({ name: `${a.action}: other`, priority: p++, conditions: [toolAvail(t)], response: S(hint) });
  }
  out.push({ name: 'any other prompt', priority: 900, conditions: [], response: S(hint) });
  return out;
}

export const llmScenarios = (u) => (u.version === 'v1' ? v1Scenarios(u) : v2Scenarios(u));
