import React, { Component } from 'react';
import Draggable from 'react-draggable';

class WhiteKing extends Component {
    constructor(props) {
        super(props)
        this.state = {
            gridPosition: {
                x: 0,
                y: 0
            }
        }
        this.tileSize = props.tileSize;
        this.matrixPos = this.props.pos;
    }
    
    onStart = () => {
        // console.log(this.state.pos);
        let activeDrags = this.state.activeDrags
        this.setState({activeDrags: ++activeDrags});
    }

    onStop = (event, drag) => {
        let activeDrags = this.state.activeDrags
        this.setState({activeDrags: --activeDrags});
    }

    adjustPos = (pos) => {
        let new_pos;
        if(Math.abs(pos % this.tileSize) > Math.floor(this.tileSize/2)) {
            if(pos > 0) {
                new_pos = pos + (this.tileSize - (pos % this.tileSize));
            } else {
                new_pos = pos - (this.tileSize + (pos % this.tileSize));
            }
        } else {
            new_pos = pos - (pos % this.tileSize);
        }
        return new_pos
    }

    onControlledDrag = (e, position) => {
        let {x, y} = position;
        console.log("position", position);
        let oldGridX = this.state.gridPosition.x;
        let oldGridY = this.state.gridPosition.y;

        x = this.adjustPos(x);
        y = this.adjustPos(y);

        this.setState({gridPosition: {x, y}});
    
        let newRow = ((y - oldGridY) / this.tileSize) + this.matrixPos[0];
        let newCol = ((x - oldGridX) / this.tileSize) + this.matrixPos[1];
        this.matrixPos = [newRow, newCol];
    }
    
    onControlledDragStop = (e, position) => {
        this.onControlledDrag(e, position);
        this.onStop();
    }
    
    render() {
        console.log("Rendering black bishop");
        console.log("Controlled Position", this.state.gridPosition);
        console.log("Position", this.matrixPos);
        const gridPosition = this.state.gridPosition;
        const dragHandlers = {onStart: this.onStart, onStop: this.onControlledDragStop};
        return(
            <Draggable disabled={false} position={gridPosition} bounds="parent" {...dragHandlers}>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45" height="100%">
                    <g
                        fill="none"
                        fillRule="evenodd"
                        stroke="#000"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round">
                        <path d="M22.5 11.63V6M20 8h5" strokeLinejoin="miter" />
                        <path
                        d="M22.5 25s4.5-7.5 3-10.5c0 0-1-2.5-3-2.5s-3 2.5-3 2.5c-1.5 3 3 10.5 3 10.5"
                        fill="#fff"
                        strokeLinecap="butt"
                        strokeLinejoin="miter"
                        />
                        <path
                        d="M11.5 37c5.5 3.5 15.5 3.5 21 0v-7s9-4.5 6-10.5c-4-6.5-13.5-3.5-16 4V27v-3.5c-3.5-7.5-13-10.5-16-4-3 6 5 10 5 10V37z"
                        fill="#fff"
                        />
                        <path d="M11.5 30c5.5-3 15.5-3 21 0M11.5 33.5c5.5-3 15.5-3 21 0M11.5 37c5.5-3 15.5-3 21 0" />
                    </g>
                </svg>
            </Draggable>
        );
    }
}

export default WhiteKing;