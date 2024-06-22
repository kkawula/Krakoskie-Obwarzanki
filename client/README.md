## Prerequisites

- nvm
- yarn

## Running

1. Run `nvm use`, if it fails install the version of node listed in the error or check the `.nvmrc` file for the version of node to use.
1. Run `yarn` to install dependencies.
1. Run `yarn start` to start the development server.

## Development

Lint and prettier have been installed. You can use `yarn lint` and `yarn prettier` to check and format your code. These commands are set up to attempt to fix any errors they find, but they may not fix everything. Please review the output of these commands and make any necessary code edits.

These commands are automatically executed before each commit, thanks to [Husky](https://typicode.github.io/husky/), so you don't need to worry about them. However, please note that these hooks only apply to files in the staged area for faster runtime. They are also executed in the CI pipeline using Github Actions.

## Testing

Tests have not been implemented yet.
