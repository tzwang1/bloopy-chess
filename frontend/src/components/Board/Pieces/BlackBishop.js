import React, { Component } from 'react';
// import bB from './icons/bB.svg';
import Draggable from 'react-draggable';

class BlackBishop extends Component {
    constructor(props) {
        super(props)
        this.state = {
            deltaPosition: {
                x: 0,
                y: 0
            },
            controlledPosition: {
                x:0,
                y:0
            },
            pos: this.props.pos
        }
        this.tileSize = props.tileSize;
    }

    handleDrag = (e, ui) => {
        const {x, y} = this.state.deltaPosition;
        this.setState({
          deltaPosition: {
            x: x + ui.deltaX,
            y: y + ui.deltaY,
          }
        });

    }
    
    onStart = () => {
        // console.log(this.state.pos);
        let activeDrags = this.state.activeDrags
        this.setState({activeDrags: ++activeDrags});
    }

    onStop = (event, drag) => {
        console.log("In onStop");
        let activeDrags = this.state.activeDrags
        this.setState({activeDrags: --activeDrags});
    }

    onControlledDrag = (e, position) => {
        console.log("In onControlledDrag");
        let {x, y} = position;
       
        if(x % this.tileSize > 35) {
            x = x + (this.tileSize - (x % this.tileSize));
        } else {
            x = x - (x % this.tileSize);
        }

        if(y % this.tileSize > 35) {
            y = y + (this.tileSize - (y % this.tileSize));
        } else {
            y = y - (y % this.tileSize);
        }
        this.setState({controlledPosition: {x, y}});
    }
    
    onControlledDragStop = (e, position) => {
        console.log("In onControlledDragStop");
        this.onControlledDrag(e, position);
        this.onStop();
    }
    
    render() {
        console.log("Rendering black bishop");
        const controlledPosition = this.state.controlledPosition;
        const dragHandlers = {onStart: this.onStart, onStop: this.onControlledDragStop};
        return(
            <Draggable disabled={false} position={controlledPosition} bounds="parent" onDrag={this.handleDrag} {...dragHandlers}>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45" height="100%">
                    <g
                        fill="none"
                        fillRule="evenodd"
                        stroke="#000"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round">
                        <g fill="#000" strokeLinecap="butt">
                        <path d="M9 36c3.39-.97 10.11.43 13.5-2 3.39 2.43 10.11 1.03 13.5 2 0 0 1.65.54 3 2-.68.97-1.65.99-3 .5-3.39-.97-10.11.46-13.5-1-3.39 1.46-10.11.03-13.5 1-1.354.49-2.323.47-3-.5 1.354-1.94 3-2 3-2z" />
                        <path d="M15 32c2.5 2.5 12.5 2.5 15 0 .5-1.5 0-2 0-2 0-2.5-2.5-4-2.5-4 5.5-1.5 6-11.5-5-15.5-11 4-10.5 14-5 15.5 0 0-2.5 1.5-2.5 4 0 0-.5.5 0 2z" />
                        <path d="M25 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 1 1 5 0z" />
                        </g>
                        <path d="M17.5 26h10M15 30h15m-7.5-14.5v5M20 18h5" stroke="#fff" strokeLinejoin="miter" />
                    </g>
                </svg>
            </Draggable>
        );
    }
}

export default BlackBishop;