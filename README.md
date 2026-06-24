# Tech Titans CSPB-3308 Summer 2026 Project

- Team #5 Team Name: Tech Titans
- Product Name: Brick Oracle
- Meets: Tuesdays @ 5pm (MST)

## Members

- Theodore Matthews
  - User: tmatthews092
  - Email: theodore.matthews@colorado.edu
- Owen Ahlers
  - User: oahlers226
  - Email: owen@owenahlers.com
- James Tillman
  - User: horaciovelvetine
  - Email: James.Tillman@colorado.edu
- Woobin Huh
  - User: woobinhuh-creator
  - Email: woobinhuh@gmail.com

## Vision Statement

A Lego collection may be a world of creative possibilities, but it's impossible to know if you've got everything you're going to need for that next build in that uncatalogued mess of a bin. Enter, Brick Oracle: a searchable Lego cataloging web app that helps you keep track of your growing collection. An easy-to-use dashboard with tools to: import your sets, search for pieces, manage a collection, and plan out builds before the bricks hit the baseplate.

## Motivation

No matter the size of the Lego collection it can be hard to stay organized and know what you already have. With old sets sitting in storage builders will spend money on new sets and acquire piles of pieces that remain mostly unused. An easy to search inventory system can extend the useful life of a collection by highlighting new set building possibilities using existing pieces, reduce duplicate acquisitions, and save money spent on under used Legos. This, combined with a huge third-party community of enthusiast releasing their own non-Lego affiliated sets, and an old collection can quickly become a treasure trove of exciting new builds.

## Project Risks

- Scope Creep: As 4 enthusiasts for Lego ourselves it's easy to get excited and over estimate the amount of work which can be completed within the allotted time.
- New Technology: Several of the languages intended to be used are unfamiliar for a majority of the group including Flask, SQL, HTML, and CSS.
- Team Dynamics: None of the team has ever worked together and did not know each other prior to this class.
- Infrastructure: This application will require access to a shared data set which at a minimum contains the complete catalog of Lego pieces. It's currently unclear how that will be stored, persisted, and shared across the team throughout the dev process.
- Research: With such a large enthusiastic community there likely already exists some standardized ways of representing Lego in the digital space. We'll need to understand and incorporate these existing axioms to provide a well built and useable tool.

## Mitigation Strategies

- Workflow: Using project management tools and following some established conventions we intend to isolate active work into named branches leveraging the GitHub projects features. This should help ensure consistent workflow across the team to help keep track of the common goal and progress.
- Priority Ordering: Features have been discussed and arranged in priority of completion at a high level to ensure that there is enough work to do throughout the entire project, and a clear path towards an achievable MVP.
- Communication: Team communication will happen through Discord which should provide a much lower barrier to communicate casually and asynchronously.
- Planning: Initial storyboarding and framing of key components and features should allow the team to all agree on a shared vision for the outcome before the build phase and ensure we are aligned on outcome.
- Initial Resources: A large part of this build requires research and accquiring a catalogue of existing pieces, and we've already found some of these resources.
  - https://www.bricklink.com/catalogTree.asp?itemType=P
  - https://rebrickable.com/downloads/

## Development Methods

The team will follow an Agile, sprint-based approach with weekly planning meetings, short development iterations, and continuous integration. Work will be decomposed into small, independently testable components to enable rapid feedback and adapation as the project evolves. Progress will be tracked via GitHub Kanban board with each sprint ending in a review to access deliverables and reprioritize if needed.

## Development Steps

1. Define project epics, user stories, and functional and non-functional requirements.
2. Design database schema for users, user brick collection, lego sets, bricks, and build instructions.
3. Implement backend API endpoints for user functions such as lego set search and brick collection upload.  
4. Build frontend components such as catalogue search, set views, and brick collection upload and view.
5. Integrate frontend and backend components together.
6. Conduct UAT. Loop on bugs found, fixes, and testing until the team is satisfied with behavior and functionality.
7. Prepare final presentation and documentation.

## Tracking Details

Kanban boarding using GitHub's project tool (attached to this repository) available [here](https://github.com/users/horaciovelvetine/projects/7). Tickets are created via a GitHub issue for the project repo [here](https://github.com/horaciovelvetine/tech-titans-CSPB3308-project/issues). To be included in the Kanban board for the project the issue must include the 'project' using the issue sidebar UI - after being included in the project it can be assigned to any: milestone, priority, label, or team member in addition to the ability to split any large issue into sub-issues. This provides a means for tracking responsibilities and updates in a shared space, seeing other team members progress, and comments for review and discussion.

## Technology Stack

### Frontend
- HTML/CSS for layout and styling
- JavaScript with React for interactive UI components

### Backend
- Python with Flask for RESTful API development

### Database
- SQLite for development with the option to migrate to PostgreSQL
