import React, { Component } from 'react';
import Draggable from 'react-draggable';

class WhiteKnight extends Component {
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
        // console.log("position", position);
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
        // console.log("Rendering black bishop");
        // console.log("Controlled Position", this.state.gridPosition);
        // console.log("Position", this.matrixPos);
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
                        <path d="M22 10c10.5 1 16.5 8 16 29H15c0-9 10-6.5 8-21" fill="#fff" />
                        <path
                        d="M24 18c.38 2.91-5.55 7.37-8 9-3 2-2.82 4.34-5 4-1.042-.94 1.41-3.04 0-3-1 0 .19 1.23-1 2-1 0-4.003 1-4-4 0-2 6-12 6-12s1.89-1.9 2-3.5c-.73-.994-.5-2-.5-3 1-1 3 2.5 3 2.5h2s.78-1.992 2.5-3c1 0 1 3 1 3"
                        fill="#fff"
                        />
                        <path d="M9.5 25.5a.5.5 0 1 1-1 0 .5.5 0 1 1 1 0z" fill="#000" />
                        <path
                        d="M14.933 15.75a.5 1.5 30 1 1-.866-.5.5 1.5 30 1 1 .866.5z"
                        fill="#000"
                        strokeWidth="1.49997"
                        />
                    </g>
                </svg>
            </Draggable>
        );
    }
}

export default WhiteKnight;