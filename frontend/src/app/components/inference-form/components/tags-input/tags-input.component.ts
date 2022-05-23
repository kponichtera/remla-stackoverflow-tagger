import {Component, EventEmitter, Input, Output} from '@angular/core';
import {MatChipInputEvent} from "@angular/material/chips";
import {FormControl} from "@angular/forms";
import {COMMA, ENTER} from "@angular/cdk/keycodes";

@Component({
  selector: 'app-tags-input',
  templateUrl: './tags-input.component.html',
  styleUrls: ['./tags-input.component.scss']
})
export class TagsInputComponent  {

  separatorKeysCodes: number[] = [ENTER, COMMA];

  private _newTag: string = ''

  @Input()
  disabled: boolean = false;

  @Input()
  tags: Set<string> = new Set<string>();

  @Output()
  tagsChange = new EventEmitter<Set<string>>();

  @Output()
  newTagChange = new EventEmitter<string>();

  constructor() { }

  add(): void {
    const value = this._newTag.trim();

    if (value) {
      this.tags.add(value);
      this.tagsChange.emit(this.tags);
    }

    // Clear the input value
    this._newTag = ''
  }

  remove(tag: string): void {
    let removed = this.tags.delete(tag)
    if (removed) {
      this.tagsChange.emit(this.tags)
    }
  }

  @Input()
  get newTag(): string {
    return this._newTag;
  }

  set newTag(value: string) {
    this._newTag = value;
    this.newTagChange.emit(value);
  }

}
